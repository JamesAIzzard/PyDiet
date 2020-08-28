import pydiet

class InvalidNutrientAmountsError(pydiet.exceptions.PyDietException):
    pass

class NutrientQtyExceedsIngredientQtyError(pydiet.exceptions.PyDietException):
    pass

class NutrientConstituentsExceedGroupError(pydiet.exceptions.PyDietException):
    pass

class NutrientAmountUndefinedError(pydiet.exceptions.PyDietException):
    pass