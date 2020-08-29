from typing import Optional

import pydiet

class NutrientConfigsError(pydiet.exceptions.PyDietException):
    def __init__(self, message:Optional[str]):
        self.message = message

class UnknownNutrientNameError(pydiet.exceptions.PyDietException):
    pass

class InvalidNutrientAmountsError(pydiet.exceptions.PyDietException):
    pass

class NutrientQtyExceedsIngredientQtyError(pydiet.exceptions.PyDietException):
    pass

class NutrientConstituentsExceedGroupError(pydiet.exceptions.PyDietException):
    pass

class NutrientAmountUndefinedError(pydiet.exceptions.PyDietException):
    pass