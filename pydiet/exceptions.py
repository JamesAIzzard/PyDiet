class PyDietException(Exception):
    pass


class PercentageSumError(PyDietException, ValueError):
    pass


class InvalidPositivePercentageError(PyDietException, ValueError):
    ...
