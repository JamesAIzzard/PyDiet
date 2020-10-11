from typing import Dict, Callable, Optional

import pydiet
from pydiet.ingredients import HasSettableIngredientAmounts
from pyconsoleapp import PrimaryArg, StandardPageComponent, menu_tools

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

        self._subject: Optional['HasSettableIngredientAmounts']
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

    def _on_load(self) -> None:
        self._ingredient_num_map = menu_tools.create_number_name_map(self._subject.constituent_ingredient_names)

    def _get_ingredient_name(self, num: int) -> str:
        return self._ingredient_num_map[num]

    def _print_main_view(self) -> str:
        return self.app.get_component(StandardPageComponent).print_view(
            page_title='Ingredients List Editor',
            page_content=_main_view_template.format(ingredient_menu=self._ingredient_menu)
        )

    def _ingredient_menu(self) -> str:
        menu = ''
        if len(self._subject.constituent_ingredients):
            for num in self._ingredient_num_map:
                menu = menu + '{num:<4} {name}\n'.format(num=str(num)+'.', name=self._get_ingredient_name(num))
        else:
            menu = 'No ingredients to show yet.'
        return menu

    def _on_add_ingredient(self, args) -> None:
        ...

    def _on_remove_ingredient(self, args) -> None:
        ...

    def configure(self, subject: 'HasSettableConstituentIngredients', return_to_route: str,
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


class IngredientDetailEditor(pydiet.cli_components.BaseEditorComponent):
    def __init__(self, app):
        super().__init__(app)
