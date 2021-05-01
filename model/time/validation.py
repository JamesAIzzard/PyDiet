import time


def validate_time(time_string: str) -> str:
    """Checks the string can be interpreted as a 24hr time."""
    # See if the time module can parse it;
    try:
        time.strptime(time_string, "%H:%M")
    # It can't, so just re-raise the error;
    except ValueError as err:
        raise err
    # No errors so must have been OK, return the string;
    return time_string
