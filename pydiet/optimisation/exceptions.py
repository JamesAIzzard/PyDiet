class DayGoalsNotFoundError(ValueError):
    def __init__(self, *args):
        if len(args) and args[0]:
            super().__init__(args[0])

class DayGoalsNameUndefinedError(ValueError):
    def __init__(self, *args):
        if len(args) and args[0]:
            super().__init__(args[0])            

class DuplicateMealGoalsNameError(ValueError):
    def __init__(self, *args):
        if len(args) and args[0]:
            super().__init__(args[0])                

class DuplicateDayGoalsNameError(ValueError):
    def __init__(self, *args):
        if len(args) and args[0]:
            super().__init__(args[0])                   