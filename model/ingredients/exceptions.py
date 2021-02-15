import model


class DuplicateIngredientNameError(model.exceptions.PyDietException):
    pass


class IngredientNameUndefinedError(model.exceptions.PyDietException):
    pass


class IngredientNotFoundError(model.exceptions.PyDietException):
    pass
