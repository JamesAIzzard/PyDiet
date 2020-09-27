from pyconsoleapp import search_tools, menu_tools
from pyconsoleapp.builtin_components import base_search_component
from pydiet import persistence, ingredients


class IngredientSearchComponent(base_search_component.BaseSearchComponent):

    def __init__(self, app):
        super().__init__(app)

    def _on_search(self, args) -> None:
        results = search_tools.search_n_best_matches(
            persistence.persistence_service.get_saved_unique_vals(ingredients.ingredient.Ingredient),
            args['search_term'], 5)
        self._results_num_map = menu_tools.create_number_name_map(results)
        self.change_state('results')
