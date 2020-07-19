import pydiet

class DuplicateIngredientNameError(pydiet.exceptions.PyDietException):
    pass


class IngredientNameUndefinedError(pydiet.exceptions.PyDietException):
    pass


class IngredientNotFoundError(pydiet.exceptions.PyDietException):
    pass


class IngredientDensityUndefinedError(pydiet.exceptions.PyDietException):
    pass



