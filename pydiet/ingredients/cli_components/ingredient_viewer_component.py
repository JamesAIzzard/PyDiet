from typing import List

from pydiet import persistence, ingredients
from pydiet.cli_components import BaseViewerComponent


class IngredientViewerComponent(BaseViewerComponent):
    def __init__(self, app):
        super().__init__(app=app, item_type=ingredients.ingredient.Ingredient,
                         item_editor_route='home.ingredients.edit')

    @property
    def _get_saved_unique_vals(self) -> List[str]:
        return persistence.persistence_service.get_saved_unique_vals(ingredients.ingredient.Ingredient)
