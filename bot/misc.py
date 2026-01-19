# Misc functions


def get_update_type(update: dict, allowed_update_types) -> str | None:

    for key in update:
        if key in allowed_update_types:
            return key

    return None


def get_bizmsg_type(update: dict, allowed_bizmsg_types) -> str | None:
    bm = update.get("business_message") or update.get("edited_business_message") or {}

    for key in bm:
        if key in allowed_bizmsg_types:
            return key

    return None


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
