from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydiet.ingredients.ingredient import Ingredient


class IngredientAmount():

    def __init__(self):
        self.ingredient: 'Ingredient'
        self.quantity: float
        self.quantity_units: str
        self.perc_increase:float
        self.perc_decrease:float