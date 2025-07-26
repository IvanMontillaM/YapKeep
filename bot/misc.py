import datetime
import os

# To determine message type, we disregard the following list of keys. What should remain, is the message type,
# whether it's text, audio, voice, photo, among others.
#
# Source: https://core.telegram.org/bots/api#message
disallowed_keys_on_msg = [
    "message_id",
    "message_thread_id",
    "from",
    "sender_chat",
    "sender_boost_count",
    "sender_business_bot",
    "date",
    "business_connection_id",
    "chat",
    "forward_origin",
    "is_topic_message",
    "is_automatic_forward",
    "reply_to_message",
    "external_reply",
    "quote",
    "reply_to_story",
    "via_bot",
    "edit_date",
    "has_protected_content",
    "is_from_offline",
    "media_group_id",
    "author_signature",
    "paid_star_count",
    "text",
    "entities",
    "link_preview_options",
    "effect_id",
    "animation",
    "paid_media",
    "sticker",
    "story",
    "caption",
    "caption_entities",
    "show_caption_above_media",
    "has_media_spoiler",
    "checklist",
    "contact",
    "dice",
    "game",
    "poll",
    "venue",
    "location",
    "new_chat_members",
    "left_chat_member",
    "new_chat_title",
    "new_chat_photo",
    "delete_chat_photo",
    "group_chat_created",
    "supergroup_chat_created",
    "channel_chat_created",
    "message_auto_delete_timer_changed",
    "migrate_to_chat_id",
    "migrate_from_chat_id",
    "pinned_message",
    "invoice",
    "successful_payment",
    "refunded_payment",
    "users_shared",
    "chat_shared",
    "gift",
    "unique_gift",
    "connected_website",
    "write_access_allowed",
    "passport_data",
    "proximity_alert_triggered",
    "boost_added",
    "chat_background_set",
    "checklist_tasks_done",
    "checklist_tasks_added",
    "direct_message_price_changed",
    "forum_topic_created",
    "forum_topic_edited",
    "forum_topic_closed",
    "forum_topic_reopened",
    "general_forum_topic_hidden",
    "general_forum_topic_unhidden",
    "giveaway_created",
    "giveaway",
    "giveaway_winners",
    "giveaway_completed",
    "paid_message_price_changed",
    "video_chat_scheduled",
    "video_chat_started",
    "video_chat_ended",
    "video_chat_participants_invited",
    "web_app_data",
    "reply_markup",
]


def str_to_bool(val):
    """Convert a string representation of truth to true (1) or false (0).
    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()

    if val in ("y", "yes", "t", "true", "on", "1"):
        bool_value = 1
    elif val in ("n", "no", "f", "false", "off", "0"):
        bool_value = 0
    else:
        raise ValueError(f"invalid truth value {(val,)}")

    return bool_value


def date_to_str(d: datetime, fmt: str) -> str:
    """Function imported from a previous project.

    Unclear why it was needed, but I suspect because of the difference between Dev platform and Prod environment.

    :param d: The datetime object
    :param fmt: The format to string
    :return: The string formatted
    """
    # locale.setlocale(locale.LC_ALL, "es_VE")
    return d.strftime(fmt.replace("%-", "%#") if os.name == "nt" else fmt)
