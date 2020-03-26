from typing import TYPE_CHECKING, Optional

from pinjector import inject

if TYPE_CHECKING:
    from pydiet.ingredients.ingredient import Ingredient
    from pydiet.ingredients.ingredient_service import IngredientService
    from pyconsoleapp import ConsoleApp

# Ingredient being edited;
ingredient: 'Ingredient'

# Temp storage for cost data;
cost_mass: float
cost_mass_units: str
cost: float


def show_ingredient_summary() -> None:
    if ingredient:
        app: 'ConsoleApp' = inject('pydiet.app')
        ingredient_service: 'IngredientService' = inject(
            'pydiet.ingredient_service')
        app.set_window_text(
            ingredient_service.summarise_ingredient(ingredient)
        )
        app.show_text_window()
