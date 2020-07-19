import pydiet

class NutrientQtyExceedsIngredientQtyError(pydiet.PyDietException):
    pass

class NutrientConstituentsExceedGroupError(pydiet.PyDietException):
    pass

class NutrientAmountUndefinedError(pydiet.PyDietException):
    pass