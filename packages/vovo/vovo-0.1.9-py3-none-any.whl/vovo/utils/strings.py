from typing import Any, List


def stringify_value(val: Any) -> str:
    """Stringify a value.

    Args:
        val: The value to stringify.

    Returns:
        str: The stringifies value.
    """
    if isinstance(val, str):
        return val
    elif isinstance(val, dict):
        return "\n" + stringify_dict(val)
    elif isinstance(val, list):
        return "\n".join(stringify_value(v) for v in val)
    else:
        return str(val)


def stringify_dict(data: dict) -> str:
    """Stringify a dictionary.

    Args:
        data: The dictionary to stringify.

    Returns:
        str: The stringifies dictionary.
    """
    text = ""
    for key, value in data.items():
        text += key + ": " + stringify_value(value) + "\n"
    return text


def join_with_separator(items: List[Any], separator: str = ", ") -> str:
    """Convert a list to a string separated by a custom separator.

    Args:
        items: The list to convert.
        separator: The string to use as a separator, default is ', '.

    Returns:
        str: The separated string.
    """
    return separator.join(str(item) for item in items)
