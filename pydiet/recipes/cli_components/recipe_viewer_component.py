from typing import List

from pydiet import persistence, recipes
from pydiet.cli_components import BaseViewerComponent


class RecipeViewerComponent(BaseViewerComponent):
    def __init__(self, app):
        super().__init__(app=app, item_type=recipes.Recipe, item_editor_route='home.recipes.edit')

    @property
    def _get_saved_unique_vals(self) -> List[str]:
        return persistence.core.get_saved_unique_vals(recipes.Recipe)
