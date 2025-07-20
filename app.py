import datetime
import json
import logging.config
import os

import requests as rq
from flask import Flask, request
from flask_executor import Executor

from bot import misc

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Set variables from environment variables
BOT_WEBHOOK_KEY = os.getenv("BOT_WEBHOOK_KEY").strip()
BOT_TGID = int(os.getenv("TG_API_KEY").strip().split(":")[0])
IS_PRETTYPRINT = bool(misc.str_to_bool(os.getenv("OPT_PRETTYPRINT").strip()))
TG_OUTPUT_CHAT_ID = os.getenv("TG_OUTPUT_CHAT_ID").strip()
API_ENDPOINT = "https://api.telegram.org/bot" + os.getenv("TG_API_KEY").strip()

# Set application configuration
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = IS_PRETTYPRINT

# Set threading pool
THREAD_EXCEPTIONS_ECHO = bool(
    misc.str_to_bool(os.getenv("THREAD_EXCEPTIONS_ECHO").strip())
)
app.config["EXECUTOR_PROPAGATE_EXCEPTIONS"] = THREAD_EXCEPTIONS_ECHO
e = Executor(app)


# Main webhook to receive notifications from Telegram
@app.route(f"/webhook/{BOT_WEBHOOK_KEY}", methods=["POST"])
def webhook():
    """Main webhook to receive Telegram notifications.

    :return: A response that Telegram understands as a chat action or answer callback query message
    """
    if request.method == "POST":
        # Insert raw payload into a variable
        tg_payload = request.data.decode("utf-8")
        # Parse payload body as JSON, it becomes the notification coming from Telegram
        tg_notification = json.loads(tg_payload)
        # Live print of the JSON payload, done with print() because of encoding errors
        print(
            str(datetime.datetime.now()).replace(".", ",")[:-3],
            f"New update: {json.dumps(tg_notification)}",
        )

        message = {
            "first_name": tg_notification["business_message"]["from"]["first_name"],
            "user_id": tg_notification["business_message"]["from"]["id"],
            "message_id": tg_notification["business_message"]["message_id"],
            "text": tg_notification["business_message"]["text"],
        }

        # Set appropriate Telegram api_method to call
        api_method = API_ENDPOINT + "/sendMessage"

        # Prepare request params
        params = {
            "chat_id": TG_OUTPUT_CHAT_ID,
            # "parse_mode": "Markdown",
            "disable_web_page_preview": 1,
            "text": (
                f"{message['first_name']} ({message["user_id"]}) said (id: {message['message_id']}):\n\n"
                f"{message['text']}"
            ),
        }

        rq.post(
            api_method,
            params=params,
        )

    response = "OK"
    return response, 200


@app.route("/", methods=["GET"])
def bot_index():
    """Redirection to the main website in case the server is hit with browser requests on the main
    route.

    :return: Returns a redirect to the main website
    """
    redirection_http_code, redirection_http_message = (301, "Moved Permanently")
    remote_addr = request.environ.get("HTTP_X_REAL_IP", request.remote_addr)
    redirect = '<head><meta http-equiv="refresh" content="0; URL=\'https://www.bing.com\'" /></head>'
    logger.info(
        "%s hit the main route; Redirecting (%s %s)",
        remote_addr,
        redirection_http_code,
        redirection_http_message,
    )
    logger.info("%s", app.url_map)
    return redirect, redirection_http_code


# Application's main entry point (app.py:app)
if __name__ == "__main__":
    app.run()
