from pyconsoleapp import search_tools, menu_tools, builtin_components
from pydiet import nutrients


class NutrientSearchComponent(builtin_components.base_search_component.BaseSearchComponent):

    def __init__(self, app):
        super().__init__(app)

    @property
    def _results_menu(self) -> str:
        results_menu = ''

        for result_num in self._results_num_map:
            result_name = self._result_name_from_num(result_num)
            alias_summary = ''
            primary_name = nutrients.nutrients_service.get_nutrient_primary_name(result_name)
            if not primary_name == result_name:
                alias_summary = ' (alias for {})'.format(primary_name)
            results_menu = results_menu + '{num}. {nutrient_name}{alias_summary}\n'.format(
                num=result_num, nutrient_name=result_name, alias_summary=alias_summary
            )
        return results_menu

    def _on_search(self, args) -> None:
        results = search_tools.search_n_best_matches(
            nutrients.nutrients_service.all_primary_and_alias_nutrient_names(),
            args['search_term'], 5)
        self._results_num_map = menu_tools.create_number_name_map(results)
        self.change_state('results')
