import logging

# for various utility functions


def json_get_by_id(json: list, id: int):
    """
    Find and return the first object in a JSON list that matches a given ID.

    Parameters:
        json (list): A list of JSON objects.
        id (int): The ID to search for.

    Returns:
        dict or None: The first object in the JSON list that matches the given ID, or None if no match is found.
    """

    return next((obj for obj in json if obj['id'] == id), None)


def trim_str(string: str, length: int) -> str:
    """
    Trims a string to a given length if needed.

    Parameters:
        string (str): The string to trim.
        length (int): The length to trim to.

    Returns:
        str: The trimmed string.
    """
    if len(string) > length:
        return string[:length - 3] + '...'
    return string


def trim_for_button(text):
    """ Trims text to fit telegram buttons """
    return trim_str(text, 32)


def trim_for_caption(text):
    """ Trims text to fit telegram captions """
    return trim_str(text, 1024)


def trim_for_message(text):
    """ Trims text to fit telegram message """
    return trim_str(text, 4096)
