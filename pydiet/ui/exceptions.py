class UnknownViewError(Exception):
    def __init__(self, message, choice):
        super().__init__(message)
        self.message = message
        self.choice = choice