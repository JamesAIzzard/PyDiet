from typing import TYPE_CHECKING, Dict, List

if TYPE_CHECKING:
    from pydiet.ingredients.ingredient_amount import IngredientAmount


class Recipe():

    def __init__(self):
        self.name: str
        self.ingredient_amounts: Dict[str, 'IngredientAmount']
        self.serve_between: List[str]
        self.categories: List[str]
