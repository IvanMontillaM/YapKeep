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


# Main webhook to receive updates from Telegram
@app.route(f"/webhook/{BOT_WEBHOOK_KEY}", methods=["POST"])
def webhook():
    """Main webhook to receive Telegram updates.

    :return: A response that Telegram understands as a chat action or answer callback query message.
    """
    if request.method == "POST":
        # Insert raw payload into a variable
        tg_payload = request.data.decode("utf-8")
        # Parse payload body as JSON, it becomes the notification coming from Telegram
        tg_update = json.loads(tg_payload)

        # Live print of the JSON payload, done with print() because of encoding errors
        print(
            str(datetime.datetime.now()).replace(".", ",")[:-3],
            f"New update: {json.dumps(tg_update)}",
        )

        # Extract JSON keys and set the update type based on keys present
        tg_notification_keys = tg_update.keys()
        tg_update_type = ""
        for key in tg_notification_keys:
            disallowed_keys = ["update_id"]
            if key not in disallowed_keys:
                tg_update_type = key

        # If not in allowed, handled list, early return
        allowed_update_types = [
            "business_message",
            "edited_business_message",
            "deleted_business_messages",
        ]
        if tg_update_type not in allowed_update_types:
            response = "OK"
            return response, 200

        if tg_update_type == "business_message":

            # Extract JSON keys and set the business message type based on keys present
            tg_bizmsg_keys = tg_update[tg_update_type].keys()
            tg_bizmsg_type = ""
            for key in tg_bizmsg_keys:
                disallowed_keys = [
                    "business_connection_id",
                    "message_id",
                    "from",
                    "chat",
                    "date",
                ]
                if key not in disallowed_keys:
                    tg_bizmsg_type = key

            # If not in allowed, handled list, early return
            allowed_bizmsg_types = [
                "text",
                "photo",
                "video",
            ]
            if tg_bizmsg_type not in allowed_bizmsg_types:
                response = "OK"
                return response, 200

            api_method = ""
            params = {}
            # Business message text handler
            if tg_bizmsg_type == "text":
                message = {
                    "first_name": tg_update["business_message"]["from"]["first_name"],
                    "user_id": tg_update["business_message"]["from"]["id"],
                    "message_id": tg_update["business_message"]["message_id"],
                    "text": tg_update["business_message"]["text"],
                }

                # Set appropriate Telegram api_method to call
                api_method = API_ENDPOINT + "/sendMessage"

                # Prepare request params
                params = {
                    "chat_id": TG_OUTPUT_CHAT_ID,
                    # "parse_mode": "Markdown",
                    "disable_web_page_preview": 1,
                    "text": (
                        f"{message['first_name']} ({message["user_id"]}) sent (id: {message['message_id']}):\n\n"
                        f"{message['text']}"
                    ),
                }

            # Business message photo handler
            elif tg_bizmsg_type == "photo":
                message = {
                    "first_name": tg_update["business_message"]["from"]["first_name"],
                    "user_id": tg_update["business_message"]["from"]["id"],
                    "message_id": tg_update["business_message"]["message_id"],
                    "photo": tg_update["business_message"]["photo"][::-1][0]["file_id"],
                }

                # Try grabbing the caption, if applicable
                try:
                    message["caption"] = tg_update["business_message"]["caption"]
                except KeyError:
                    pass

                # Set appropriate Telegram api_method to call
                api_method = API_ENDPOINT + "/sendPhoto"

                # Prepare request params
                params = {
                    "chat_id": TG_OUTPUT_CHAT_ID,
                    # "parse_mode": "Markdown",
                    "disable_web_page_preview": 1,
                    "caption": (
                        f"{message['first_name']} ({message["user_id"]}) sent (id: {message['message_id']})"
                    ),
                    "photo": message["photo"],
                }

                try:
                    params["caption"] += f":\n\n{message['caption']}"
                except KeyError:
                    pass

            # Business message video handler
            elif tg_bizmsg_type == "video":
                message = {
                    "first_name": tg_update["business_message"]["from"]["first_name"],
                    "user_id": tg_update["business_message"]["from"]["id"],
                    "message_id": tg_update["business_message"]["message_id"],
                    "video": tg_update["business_message"]["video"]["file_id"],
                }

                # Try grabbing the caption, if applicable
                try:
                    message["caption"] = tg_update["business_message"]["caption"]
                except KeyError:
                    pass

                # Set appropriate Telegram api_method to call
                api_method = API_ENDPOINT + "/sendVideo"

                # Prepare request params
                params = {
                    "chat_id": TG_OUTPUT_CHAT_ID,
                    # "parse_mode": "Markdown",
                    "disable_web_page_preview": 1,
                    "caption": (
                        f"{message['first_name']} ({message["user_id"]}) sent (id: {message['message_id']})"
                    ),
                    "video": message["video"],
                }

                try:
                    params["caption"] += f":\n\n{message['caption']}"
                except KeyError:
                    pass

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
