import datetime
import os


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
