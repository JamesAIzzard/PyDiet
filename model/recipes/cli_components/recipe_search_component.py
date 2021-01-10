from typing import List

from pyconsoleapp.builtin_components.base_search_component import BaseSearchComponent
from pydiet import persistence, recipes


class RecipeSearchComponent(BaseSearchComponent):

    def __init__(self, app):
        super().__init__(app)

    @property
    def _data_to_search(self) -> List[str]:
        return persistence.core.get_saved_unique_vals(recipes.Recipe)