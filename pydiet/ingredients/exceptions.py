class NutrientQtyExceedsIngredientQtyError(ValueError):
    def __init__(self, *args):
        if len(args) and args[0]:
            super().__init__(args[0])


class ConstituentsExceedGroupError(ValueError):
    def __init__(self, *args):
        if len(args) and args[0]:
            super().__init__(args[0])

class FlagNutrientConflictError(ValueError):
    def __init__(self, *args):
        if len(args) and args[0]:
            super().__init__(args[0])

class DuplicateIngredientNameError(ValueError):
    def __init__(self, *args):
        if len(args) and args[0]:
            super().__init__(args[0])

class IngredientNameUndefinedError(ValueError):
    def __init__(self, *args):
        if len(args) and args[0]:
            super().__init__(args[0])

class IngredientNotFoundError(ValueError):
    def __init__(self, *args):
        if len(args) and args[0]:
            super().__init__(args[0])

class IngredientDensityUndefinedError(AttributeError):
    def __init__(self, *args):
        if len(args) and args[0]:
            super().__init__(args[0])

class NutrientAmountUndefinedError(AttributeError):
    def __init__(self, *args):
        if len(args) and args[0]:
            super().__init__(args[0])