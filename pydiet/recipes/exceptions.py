class DuplicateRecipeNameError(ValueError):
    def __init__(self, *args):
        if len(args) and args[0]:
            super().__init__(args[0])

class RecipeNameUndefinedError(ValueError):
    def __init__(self, *args):
        if len(args) and args[0]:
            super().__init__(args[0])

class RecipeNotFoundError(ValueError):
    def __init__(self, *args):
        if len(args) and args[0]:
            super().__init__(args[0])