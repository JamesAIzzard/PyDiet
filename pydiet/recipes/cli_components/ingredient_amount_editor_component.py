from typing import Dict, Callable, Optional

import pydiet
from pyconsoleapp import PrimaryArg, StandardPageComponent, menu_tools
from pydiet import persistence
from pydiet.ingredients import HasSettableIngredientAmounts, IngredientSearchComponent, Ingredient

_main_view_template = '''
OK & Save           | -ok
Cancel              | -cancel
Add Ingredient      | -add [ingredient name]
Remove Ingredient   | -del [ingredient number]

{ingredient_menu}
'''


class ConstituentIngredientEditorComponent(pydiet.cli_components.BaseEditorComponent):
    def __init__(self, app):
        super().__init__(app)

        self._subject: Optional['HasSettableIngredientAmounts'] = None
        self._ingredient_num_map: Dict[int, str] = {}

        self._configure_state('main', self._print_main_view, responders=[
            self.configure_responder(self._on_ok_and_save, args=[
                PrimaryArg('save', has_value=False, markers=['-ok'])]),
            self.configure_responder(self._on_cancel, args=[
                PrimaryArg('cancel', has_value=False, markers=['-cancel'])]),
            self.configure_responder(self._on_add_ingredient, args=[
                PrimaryArg('ingredient_name', has_value=True, markers=['-add'])]),
            self.configure_responder(self._on_remove_ingredient, args=[
                PrimaryArg('ingredient_number', has_value=True, markers=['-del'], validators=[
                    self._validate_ingredient_number])])
        ])

        self._detail_editor_component = self._use_component(['search_results'], IngredientAmountDetailEditor(app))
        self._search_component = self._use_component(['edit_detail'], IngredientSearchComponent(app))

    def _on_load(self) -> None:
        self._ingredient_num_map = menu_tools.create_number_name_map(self._subject.ingredient_names)

    def _get_ingredient_name(self, num: int) -> str:
        return self._ingredient_num_map[num]

    def _print_main_view(self) -> str:
        return self.app.get_component(StandardPageComponent).print_view(
            page_title='Ingredients List Editor',
            page_content=_main_view_template.format(ingredient_menu=self._ingredient_menu)
        )

    def _ingredient_menu(self) -> str:
        menu = ''
        if len(self._subject.ingredient_amounts_data):
            for num in self._ingredient_num_map:
                menu = menu + '{num:<4} {name}\n'.format(num=str(num) + '.', name=self._get_ingredient_name(num))
        else:
            menu = 'No ingredients to show yet.'
        return menu

    def _on_add_ingredient(self, args) -> None:
        def on_result_selected(ingredient_name: str):
            i = persistence.load(Ingredient, ingredient_name)
            self._detail_editor_component.configure(
                ingredient=i,
                recipe=self._subject)
            self.current_state = 'edit_detail'

        self._search_component.configure('ingredient', on_result_selected)
        results = self._search_component.search_for(args['ingredient_name'])
        self._search_component.load_results(results)
        self._search_component.change_state('results')
        self.change_state('search_results')

    def _on_remove_ingredient(self, args) -> None:
        i_name = self._get_ingredient_name(args['ingredient_number'])
        self._subject.remove_ingredient_amount(ingredient_name = i_name)

    def configure(self, subject: 'HasSettableIngredientAmounts', return_to_route: str,
                  revert_data: Callable) -> None:
        super()._configure(subject=subject, revert_data=revert_data, return_to_route=return_to_route)


_ingredient_add_view_template = '''
OK & Save           | -ok
Cancel              | -cancel
                    |
Set Quantity        | -qty  [quantity and unit]
                    |
Set Allowable +     | -inc [quantity and unit (or %)]
Set Allowable -     | -dec [quantity and unit (or %)]

{ingredient_summary}
'''


class IngredientAmountDetailEditor(pydiet.cli_components.BaseEditorComponent):
    def __init__(self, app):
        super().__init__(app)
