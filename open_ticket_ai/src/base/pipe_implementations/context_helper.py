import functools


def get_value_from_context(context: dict, key_string: str):
    """
    Safely gets a nested value from a dictionary using dot notation.
    """
    keys = key_string.split('.')
    try:
        # This is a safe way to do a deep-get
        return functools.reduce(lambda d, key: d[key], keys, context)
    except (KeyError, TypeError):
        # Handle cases where the path doesn't exist
        return None
