# To determine message type, we disregard the following list of keys. What should remain, is the message type,
# whether it's text, audio, voice, photo, among others.
#
# Source: https://core.telegram.org/bots/api#message
disallowed_keys_on_msg = [
    "animation",
    "author_signature",
    "boost_added",
    "business_connection_id",
    "caption",
    "caption_entities",
    "channel_chat_created",
    "chat",
    "chat_background_set",
    "chat_shared",
    "checklist",
    "checklist_tasks_added",
    "checklist_tasks_done",
    "connected_website",
    "contact",
    "date",
    "delete_chat_photo",
    "dice",
    "direct_message_price_changed",
    "direct_messages_topic",
    "edit_date",
    "effect_id",
    "entities",
    "external_reply",
    "forum_topic_closed",
    "forum_topic_created",
    "forum_topic_edited",
    "forum_topic_reopened",
    "forward_origin",
    "from",
    "game",
    "general_forum_topic_hidden",
    "general_forum_topic_unhidden",
    "gift",
    "giveaway",
    "giveaway_completed",
    "giveaway_created",
    "giveaway_winners",
    "group_chat_created",
    "has_media_spoiler",
    "has_protected_content",
    "invoice",
    "is_automatic_forward",
    "is_from_offline",
    "is_paid_post",
    "is_topic_message",
    "left_chat_member",
    "link_preview_options",
    "location",
    "media_group_id",
    "message_auto_delete_timer_changed",
    "message_id",
    "message_thread_id",
    "migrate_from_chat_id",
    "migrate_to_chat_id",
    "new_chat_members",
    "new_chat_photo",
    "new_chat_title",
    "paid_media",
    "paid_message_price_changed",
    "paid_star_count",
    "passport_data",
    "pinned_message",
    "poll",
    "proximity_alert_triggered",
    "quote",
    "refunded_payment",
    "reply_markup",
    "reply_to_checklist_task_id",
    "reply_to_message",
    "reply_to_story",
    "sender_boost_count",
    "sender_business_bot",
    "sender_chat",
    "show_caption_above_media",
    "sticker",
    "story",
    "successful_payment",
    "suggested_post_approval_failed",
    "suggested_post_approved",
    "suggested_post_declined",
    "suggested_post_info",
    "suggested_post_paid",
    "suggested_post_refunded",
    "supergroup_chat_created",
    "unique_gift",
    "users_shared",
    "venue",
    "via_bot",
    "video_chat_ended",
    "video_chat_participants_invited",
    "video_chat_scheduled",
    "video_chat_started",
    "web_app_data",
    "write_access_allowed",
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
