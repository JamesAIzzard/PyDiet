from typing import List

from pydiet.cli_components import BaseViewerComponent
from pydiet import persistence, ingredients


class IngredientViewerComponent(BaseViewerComponent):
    def __init__(self, app):
        super().__init__(app=app, item_type=ingredients.Ingredient, item_editor_route='home.ingredients.editor')

    @property
    def _get_saved_unique_vals(self) -> List[str]:
        return persistence.persistence_service.get_saved_unique_vals(ingredients.Ingredient)
