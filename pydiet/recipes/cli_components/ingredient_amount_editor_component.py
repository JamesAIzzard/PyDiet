from typing import Dict, Tuple, Callable, Optional

import pydiet
from pyconsoleapp import PrimaryArg, StandardPageComponent, menu_tools, ResponseValidationError, builtin_validators
from pydiet import persistence, quantity
from pydiet.ingredients import HasSettableIngredientAmounts, IngredientSearchComponent, Ingredient, IngredientAmountData

_main_view_template = '''
OK & Save           | -ok
Cancel              | -cancel
Add Ingredient      | -add [ingredient name]
Remove Ingredient   | -del [ingredient number]

{ingredient_menu}
'''


class IngredientAmountEditorComponent(pydiet.cli_components.BaseEditorComponent):
    def __init__(self, app):
        super().__init__(app)

        self._subject: Optional['HasSettableIngredientAmounts'] = None
        self._ingredient_num_map: Dict[int, str] = {}

        self.configure_state('main', self._print_main_view, responders=[
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

        self._detail_editor_component = self._assign_state_to_component(['edit_detail'],
                                                                        IngredientAmountDetailEditor(app))
        self._search_component = self._assign_state_to_component(['search_results'], IngredientSearchComponent(app))

    def _on_load(self) -> None:
        self._ingredient_num_map = menu_tools.create_number_name_map(self._subject.ingredient_names)

    def _get_ingredient_name(self, num: int) -> str:
        return self._ingredient_num_map[num]

    def _print_main_view(self) -> str:
        return self.app.get_component(StandardPageComponent).print_view(
            page_title='Ingredients List Editor',
            page_content=_main_view_template.format(ingredient_menu=self._ingredient_menu)
        )

    @property
    def _ingredient_menu(self) -> str:
        menu = ''
        if len(self._subject.ingredient_amounts_data):
            for num in self._ingredient_num_map:
                menu = menu + '{num:<4} {name}\n'.format(num=str(num) + '.', name=self._get_ingredient_name(num))
        else:
            menu = 'No ingredients to show yet.'
        return menu

    def _validate_ingredient_number(self, value) -> int:
        try:
            value = int(value)
        except TypeError:
            raise ResponseValidationError('Please enter a valid ingredient number.')
        if value not in self._ingredient_num_map:
            raise ResponseValidationError('Please enter a valid ingredient number.')
        return value

    def _on_add_ingredient(self, args) -> None:
        def on_result_selected(ingredient_name: str):
            i = persistence.load(Ingredient, ingredient_name)
            ingredient_amount_data = self._subject.get_ingredient_amount_data(ingredient_name=ingredient_name)
            self._detail_editor_component.configure(
                ingredient_amount_data=ingredient_amount_data,
                ingredient_name=ingredient_name,
                revert_data=lambda: self._subject.set_ingredient_amount_data(
                    data=ingredient_amount_data,
                    ingredient_name=ingredient_name
                ),
                to_exit=lambda: self.app.goto('home.recipes.edit.ingredients')
            )
            self.current_state = 'edit_detail'

        self._search_component.configure('ingredient', on_result_selected)
        results = self._search_component.search_for(args['ingredient_name'])
        self._search_component.load_results(results)
        self._search_component.change_state('results')
        self.change_state('search_results')

    def _on_remove_ingredient(self, args) -> None:
        i_name = self._get_ingredient_name(args['ingredient_number'])
        self._subject.remove_ingredient_amount(ingredient_name=i_name)

    def configure(self,
                  subject: 'HasSettableIngredientAmounts',
                  return_to_route: str,
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
        self._ingredient_amount_data: Optional['IngredientAmountData'] = None
        self._ingredient_name: Optional[str] = None

        self.configure_state('main', self._print_main_view, responders=[
            self.configure_responder(self._on_ok_and_save, args=[
                PrimaryArg('save', has_value=False, markers=['-ok'])]),
            self.configure_responder(self._on_cancel, args=[
                PrimaryArg('cancel', has_value=False, markers=['-cancel'])]),
            self.configure_responder(self._on_set_qty, args=[
                PrimaryArg('quantity', has_value=True, markers=['-qty'], validators=[self._validate_qty_and_unit])]),
            self.configure_responder(self._on_set_perc_inc, args=[
                PrimaryArg('perc_incr', has_value=True, markers=['-inc'], validators=[
                    builtin_validators.validate_positive_or_zero_number])]),
            self.configure_responder(self._on_set_perc_dec, args=[
                PrimaryArg('perc_decr', has_value=True, markers=['-dec'], validators=[
                    builtin_validators.validate_positive_or_zero_number])])
        ])

    def _print_main_view(self) -> str:
        return self.app.get_component(StandardPageComponent).print_view(
            page_title='Ingredient Amount Editor',
            page_content=_ingredient_add_view_template.format(
                ingredient_summary=
            )
        )

    def _validate_qty_and_unit(self, value: str) -> Tuple[float, str]:
        qty, unit = builtin_validators.validate_number_and_str(value)
        qty = builtin_validators.validate_positive_or_zero_number(qty)
        unit = quantity.quantity_service.validate_qty_unit(unit)
        i = persistence.load(Ingredient, self._ingredient_name)
        if quantity.quantity_service.units_are_volumes(unit) and not i.check_units_configured(unit):
            raise ResponseValidationError('Volumetric units are not yet configured for {}'.format(i.name))
        elif quantity.quantity_service.units_are_pieces(unit) and not i.check_units_configured(unit):
            raise ResponseValidationError('Piece mass has not yet been configured on {}.'.format(i.name))
        return qty, unit

    def configure(self, ingredient_amount_data: IngredientAmountData,
                  ingredient_name: str,
                  revert_data: Callable,  # Func to revert data on cancel;
                  to_exit: Callable):  # Func to leave the conponent when done;
        super()._configure(subject=None, revert_data=revert_data, to_exit=to_exit)
        self._ingredient_amount_data = ingredient_amount_data
        self._ingredient_name = ingredient_name
