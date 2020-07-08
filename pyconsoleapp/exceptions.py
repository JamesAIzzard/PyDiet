class PyConsoleAppError(Exception):
    pass

class NoPrintFunctionError(PyConsoleAppError):
    pass

class StateNotConfiguredError(PyConsoleAppError):
    pass