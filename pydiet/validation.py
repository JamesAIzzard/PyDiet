import pydiet


def validate_positive_percentage(value: float) -> None:
    try:
        value = float(value)
    except ValueError:
        raise pydiet.exceptions.InvalidPositivePercentageError
    if value < 0:
        raise pydiet.exceptions.InvalidPositivePercentageError
