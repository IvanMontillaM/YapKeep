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
            "deleted_business_messages",
            "edited_business_message",
        ]
        if tg_update_type not in allowed_update_types:
            response = "OK"
            return response, 200

        api_method = ""
        params = {}

        if (
            tg_update_type == "business_message"
            or tg_update_type == "edited_business_message"
        ):

            # Extract JSON keys and set the business message type based on keys present
            tg_bizmsg_keys = tg_update[tg_update_type].keys()
            tg_bizmsg_type = ""
            for key in tg_bizmsg_keys:
                disallowed_keys = [
                    "business_connection_id",
                    "caption",
                    "caption_entities",
                    "chat",
                    "date",
                    "entities",
                    "forward_date",
                    "forward_from_chat",
                    "forward_from_message_id",
                    "forward_origin",
                    "forward_signature",
                    "from",
                    "link_preview_options",
                    "message_id",
                    "reply_markup",
                ]
                if key not in disallowed_keys:
                    tg_bizmsg_type = key

            # If not in allowed, handled list, early return
            allowed_bizmsg_types = [
                "document",
                "photo",
                "text",
                "video",
                "video_note",
                "voice",
            ]
            if tg_bizmsg_type not in allowed_bizmsg_types:
                response = "OK"
                return response, 200

            # TODO: Add handlers for Contacts, Locations and Venues
            media_handlers = [
                "document",
                "photo",
                "video",
                "video_note",
                "voice",
            ]

            # Business message text handler
            if tg_bizmsg_type == "text":

                bizmsg = tg_update.get("business_message") or tg_update.get(
                    "edited_business_message"
                )

                message = {
                    "first_name": bizmsg["from"]["first_name"],
                    "user_id": bizmsg["from"]["id"],
                    "message_id": bizmsg["message_id"],
                    "text": bizmsg["text"],
                }

                # Set appropriate Telegram api_method to call
                api_method = API_ENDPOINT + "/sendMessage"

                caption = ""
                if tg_update_type == "business_message":
                    caption = (
                        f"{message['first_name']} ({message["user_id"]}) sent (id: {message['message_id']}):\n\n"
                        f"{message['text']}"
                    )
                elif tg_update_type == "edited_business_message":
                    caption = (
                        f"🚨 {message['first_name']} ({message["user_id"]}) edited (id: {message['message_id']}):\n\n"
                        f"{message['text']}"
                    )

                # Prepare request params
                params = {
                    "chat_id": TG_OUTPUT_CHAT_ID,
                    # "parse_mode": "Markdown",
                    "disable_web_page_preview": 1,
                    "text": caption,
                }

            # Business message with media handlers
            elif tg_bizmsg_type in media_handlers:

                bizmsg = tg_update.get("business_message") or tg_update.get(
                    "edited_business_message"
                )

                message = {
                    "first_name": bizmsg["from"]["first_name"],
                    "user_id": bizmsg["from"]["id"],
                    "message_id": bizmsg["message_id"],
                }

                if tg_bizmsg_type == "photo":
                    message[tg_bizmsg_type] = bizmsg[tg_bizmsg_type][::-1][0]["file_id"]
                else:
                    message[tg_bizmsg_type] = bizmsg[tg_bizmsg_type]["file_id"]

                # Try grabbing the caption, if applicable
                try:
                    message["caption"] = bizmsg["caption"]
                except KeyError:
                    pass

                # Video notes don't support captions, send update info separately
                if tg_bizmsg_type == "video_note":
                    # Set appropriate Telegram api_method to call
                    api_method = API_ENDPOINT + "/sendMessage"

                    # Prepare request params
                    params = {
                        "chat_id": TG_OUTPUT_CHAT_ID,
                        "text": (
                            f"{message['first_name']} ({message["user_id"]}) sent "
                            f"a video note (id: {message['message_id']}):"
                        ),
                    }

                    rq.post(
                        api_method,
                        params=params,
                    )

                # Set appropriate Telegram api_method to call
                api_method = (
                    API_ENDPOINT
                    + "/send"
                    + "".join([word.capitalize() for word in tg_bizmsg_type.split("_")])
                )

                caption = ""
                if tg_update_type == "business_message":
                    caption = f"{message['first_name']} ({message["user_id"]}) sent (id: {message['message_id']})"
                elif tg_update_type == "edited_business_message":
                    caption = f"🚨 {message['first_name']} ({message["user_id"]}) edited (id: {message['message_id']})"

                # Prepare request params
                params = {
                    "chat_id": TG_OUTPUT_CHAT_ID,
                    f"{tg_bizmsg_type}": message[tg_bizmsg_type],
                    "caption": caption,
                }

                try:
                    params["caption"] += f":\n\n{message['caption']}"
                except KeyError:
                    pass

                # Video notes don't support captions, avoid unnecessary call params
                if tg_bizmsg_type == "video_note":
                    del params["caption"]

        elif tg_update_type == "deleted_business_messages":

            bizupdate = tg_update[tg_update_type]

            message = {
                "first_name": bizupdate["chat"]["first_name"],
                "user_id": bizupdate["chat"]["id"],
                "message_ids": bizupdate["message_ids"],
            }

            api_method = API_ENDPOINT + "/sendMessage"

            # Prepare request params
            params = {
                "chat_id": TG_OUTPUT_CHAT_ID,
                # "parse_mode": "Markdown",
                "disable_web_page_preview": 1,
                "text": (
                    f"🚨 From {message['first_name']} ({message["user_id"]}) chat, "
                    "the following message IDs were deleted:\n\n"
                    f"{message["message_ids"]}"
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
