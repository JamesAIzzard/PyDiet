from typing import Optional, Dict, Any, TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent, PrimaryArg, menu_tools, StandardPageComponent, ResponseValidationError, \
    styles, builtin_validators
from pydiet import nutrients, quantity

if TYPE_CHECKING:
    from pydiet.nutrients.supports_nutrient_content import SupportsSettingNutrientContent, NutrientData

_main_menu_template = '''
OK | -ok
Cancel | -cancel

Edit Nutrient | -edit  [nutrient number]
Set New Nutrient | -new
Reset Nutrient | -reset [nutrient number]

Mandatory Nutrients:
{mandatory_nuts_menu}

Other Nutrients:
{other_nuts_menu}
'''

_edit_menu_template = '''
OK | -ok
Cancel | -cancel

Set Nutrient Amount | 
-ingr  [ingredient quantity] -nutr  [nutrient quantity]

Example: 
>>> -ingr 1.2kg -nutr 25g 
(To indicate 1.2kg of the ingredient contains 25g of 
the nutrient).

{nutrient_name}: {nutrient_summary}
'''


class NutrientContentEditorComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self._subject: Optional['SupportsSettingNutrientContent'] = None
        self._return_to_route: Optional[str] = None
        self._backup_nutrients_data: Dict[str, 'NutrientData'] = {}
        self._backup_nutrient_data: Optional['NutrientData'] = None
        self._mandatory_nuts_menu_data: Dict[int, str] = {}
        self._other_nuts_menu_data: Dict[int, str] = {}
        self._current_nutrient_name: Optional[str] = None

        self.configure_state('main', self._print_main_menu, responders=[
            self.configure_responder(self._on_main_ok, args=[
                PrimaryArg('ok', has_value=False, markers=['-ok'])]),
            self.configure_responder(self._on_main_cancel, args=[
                PrimaryArg('cancel', has_value=False, markers=['-cancel'])]),
            self.configure_responder(self._on_edit_nutrient, args=[
                PrimaryArg('edit', has_value=True, markers=['-edit'], validators=[self._validate_nutr_number])]),
            self.configure_responder(self._on_new_nutrient, args=[
                PrimaryArg('new', has_value=False, markers=['-new'])]),
            self.configure_responder(self._on_reset_nutrient, args=[
                PrimaryArg('nutr_num', has_value=True, markers=['-reset'], validators=[self._validate_nutr_number])])
        ])

        self.configure_state('edit', self._print_edit_menu, responders=[
            self.configure_responder(self._on_edit_ok, args=[
                PrimaryArg('ok', has_value=False, markers=['-ok'])]),
            self.configure_responder(self._on_edit_cancel, args=[
                PrimaryArg('cancel', has_value=False, markers=['-cancel'])]),
            self.configure_responder(self._on_set_nutrient_amount, args=[
                PrimaryArg('ingr', has_value=True, markers=['-ingr'], validators=[self._validate_ingr_input]),
                PrimaryArg('nutr', has_value=True, markers=['-nutr'], validators=[self._validate_nutr_input])
            ])
        ])

    def before_print(self) -> None:
        # Create the nutrient menus;
        self._mandatory_nuts_menu_data = menu_tools.create_number_name_map(nutrients.configs.mandatory_nutrient_names,
                                                                           start_num=1)
        self._other_nuts_menu_data = menu_tools.create_number_name_map(
            self._subject.defined_optional_nutrient_names,
            start_num=len(nutrients.configs.mandatory_nutrient_names) + 1)

    def configure(self, subject: 'SupportsSettingNutrientContent', return_to_route: str,
                  backup_nutrients_data: Dict[str, 'NutrientData']) -> None:
        self._subject = subject
        self._return_to_route = return_to_route
        self._backup_nutrients_data = backup_nutrients_data

    @property
    def _mandatory_nuts_menu(self) -> str:
        menu = ''
        for num in self._mandatory_nuts_menu_data:
            menu = menu + '{num}. {nut_name:<30} {summary:<20}\n'.format(
                num=num,
                nut_name=self._mandatory_nuts_menu_data[num].replace('_', ' ') + ':',
                summary=self._subject.summarise_nutrient(self._mandatory_nuts_menu_data[num])
            )
        return menu

    @property
    def _other_nuts_menu(self) -> str:
        if len(self._other_nuts_menu_data):
            menu = ''
            for num in self._other_nuts_menu_data:
                menu = menu + '{num}. {nut_name:<30} {summary:<20}\n'.format(
                    num=num,
                    nut_name=self._other_nuts_menu_data[num].replace('_', ' ') + ':',
                    summary=self._subject.summarise_nutrient(self._other_nuts_menu_data[num])
                )
        else:
            menu = styles.fore('No other nutrients defined yet.', 'blue')
        return menu

    def _validate_nutr_number(self, nut_num: Any) -> int:
        try:
            nut_num = int(nut_num)
        except TypeError:
            raise ResponseValidationError('Please enter a valid nutrient number.')
        if nut_num not in self._mandatory_nuts_menu_data.keys() and nut_num not in self._other_nuts_menu_data.keys():
            raise ResponseValidationError('Please enter a valid nutrient number.')
        return nut_num

    def _validate_ingr_input(self, ingr_input: str) -> Dict:
        # Split the input into number and string;
        validated_input = builtin_validators.validate_number_and_str(ingr_input)
        output = {
            'qty': validated_input[0],
            'unit': validated_input[1]
        }
        # Check the number is a valid qty;
        try:
            output['qty'] = quantity.quantity_service.validate_quantity(output['qty'])
        except quantity.exceptions.InvalidQtyError:
            raise ResponseValidationError('The ingredient quantity must be a positive number.')
        # Check the string is a valid unit;
        try:
            output['unit'] = quantity.quantity_service.validate_qty_unit(output['unit'])
        except quantity.exceptions.UnknownUnitError:
            raise ResponseValidationError('The ingredient unit is not recognised.')
        # Check the unit used has been configured
        if not self._subject.check_units_configured(output['unit']):
            if quantity.quantity_service.units_are_volumes(output['unit']):
                raise ResponseValidationError(
                    'The ingredient density must be configured before fluid measurements can be used.')
            elif quantity.quantity_service.units_are_pieces(output['unit']):
                raise ResponseValidationError(
                    'The ingredient piece mass must be configured before "pc" can be used as a unit.')
        # All OK, return.
        return output

    @staticmethod
    def _validate_nutr_input(nutr_input: str) -> Dict:
        # Split the input into number and string;
        validated_input = builtin_validators.validate_number_and_str(nutr_input)
        output = {
            'qty': validated_input[0],
            'unit': validated_input[1]
        }
        # Check the number is a valid qty;
        try:
            output['qty'] = quantity.quantity_service.validate_quantity(output['qty'])
        except quantity.exceptions.InvalidQtyError:
            raise ResponseValidationError('The nutrient quantity must be a positive number.')
        # Check the unit is a valid mass;
        try:
            output['unit'] = quantity.quantity_service.validate_mass_unit(output['unit'])
        except quantity.exceptions.UnknownUnitError:
            raise ResponseValidationError('The nutrient unit is not a recognised mass.')
        # All OK, return;
        return output

    def _print_main_menu(self) -> str:
        output = _main_menu_template.format(
            mandatory_nuts_menu=styles.fore(self._mandatory_nuts_menu, 'blue'),
            other_nuts_menu=styles.fore(self._other_nuts_menu, 'blue')
        )
        return self.app.get_component(StandardPageComponent).print(
            page_title="Nutrient Content Editor",
            page_content=output
        )

    def _print_edit_menu(self) -> str:
        output = _edit_menu_template.format(
            nutrient_name=styles.fore(self._current_nutrient_name.replace('_', ' '), 'blue'),
            nutrient_summary=styles.fore(self._subject.summarise_nutrient(self._current_nutrient_name), 'blue')
        )
        return self.app.get_component(StandardPageComponent).print(
            page_title="Nutrient Content Editor",
            page_content=output
        )

    def _get_nutr_name_from_num(self, num: int) -> str:
        if num in self._mandatory_nuts_menu_data:
            return self._mandatory_nuts_menu_data[num]
        else:
            return self._other_nuts_menu_data[num]

    def _on_main_ok(self) -> None:
        self.app.goto(self._return_to_route)

    def _on_main_cancel(self) -> None:
        self._subject.set_nutrients_data(self._backup_nutrients_data)
        self.app.goto(self._return_to_route)

    def _on_edit_nutrient(self, args) -> None:
        self._current_nutrient_name = self._get_nutr_name_from_num(args['edit'])
        self.current_state = 'edit'

    def _on_new_nutrient(self) -> None:
        nsc = self.app.get_component(nutrients.cli_components.nutrient_search_component.NutrientSearchComponent)

        def on_nutrient_selected(nutrient_name: str) -> None:
            self._current_nutrient_name = nutrient_name
            self.change_state('edit')
            self.app.goto('home.ingredients.edit.nutrients')

        nsc.configure(subject_name='Nutrient', on_result_selected=on_nutrient_selected)
        self.app.goto('home.ingredients.edit.nutrients.search')

    def _on_reset_nutrient(self, args) -> None:
        self._subject.reset_nutrient(self._get_nutr_name_from_num(args['nutr_num']))

    def _on_edit_ok(self) -> None:
        self.current_state = 'main'

    def _on_edit_cancel(self) -> None:
        self._subject.set_nutrient_data(self._current_nutrient_name, self._backup_nutrient_data)
        self.current_state = 'main'

    def _on_set_nutrient_amount(self, args) -> None:
        # Convert the args into g per g
        nutrient_qty_g = quantity.quantity_service.convert_qty_unit(
            args['nutr']['qty'],
            args['nutr']['unit'],
            'g'
        )
        ingredient_qty_g = quantity.quantity_service.convert_qty_unit(
            args['ingr']['qty'],
            args['ingr']['unit'],
            'g',
            self._subject.g_per_ml,
            self._subject.piece_mass_g
        )
        nutrient_g_per_subject_g = nutrient_qty_g / ingredient_qty_g
        # Build the correct data object;
        nutrient_data = nutrients.supports_nutrient_content.NutrientData(
            nutrient_g_per_subject_g=nutrient_g_per_subject_g,
            nutrient_pref_units=args['nutr']['unit']
        )
        # Set the data;
        self._subject.set_nutrient_data(self._current_nutrient_name, nutrient_data)
