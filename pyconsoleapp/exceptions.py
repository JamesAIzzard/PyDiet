from typing import Optional

class PyConsoleAppError(Exception):
    def __init__(self, message:Optional[str]=None):
        self.message = message

class NoPrintFunctionError(PyConsoleAppError):
    pass

class StateNotFoundError(PyConsoleAppError):
    pass

class NoPrimaryArgError(PyConsoleAppError):
    pass

class DuplicatePrimaryMarkerError(PyConsoleAppError):
    pass

class DuplicateMarkerlessArgError(PyConsoleAppError):
    pass

class DuplicateEmptyResponderError(PyConsoleAppError):
    pass

class ResponseValidationError(PyConsoleAppError):
    '''Indicates that the response is invald.'''
    def __init__(self, message:Optional[str]=None):
        super().__init__(message)

class ArgMissingValueError(ResponseValidationError):
    '''Indicates that the response is missing an arg value.'''
    def __init__(self, message:Optional[str]=None):
        super().__init__(message)

class OrphanValueError(ResponseValidationError):
    '''Indicates that there is an unexpected value in the response.'''
    def __init__(self, message:Optional[str]=None):
        super().__init__(message)