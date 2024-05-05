from typing import Any, Callable


def parse_str(
    string: str,
    key: Callable = lambda x: x,
):
    try:
        return key(string)
    except Exception:
        return None


def parse_str_with_default_if_empty(
    string: str,
    key: Callable = lambda x: x,
    default: Any | None = None,
):
    if string == "" and default is not None:
        return default

    return parse_str(string=string, key=key)
