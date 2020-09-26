from typing import Optional, Dict, Any, TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent, PrimaryArg, menu_tools, StandardPageComponent, ResponseValidationError
from pydiet import nutrients

if TYPE_CHECKING:
    from pydiet.nutrients.supports_nutrient_content import SupportsSettingNutrientContent, NutrientData

_main_menu_template = '''
----------------------------|-------------------------------
OK                          | -ok
Cancel                      | -cancel
----------------------------|-------------------------------
Edit Nutrient               | -edit  [nutrient number]
Set New Nutrient            | -new
Reset Nutrient              | -reset [nutrient number]
----------------------------|-------------------------------

Mandatory Nutrients:
{mandatory_nuts_menu}

Other Nutrients:
{other_nuts_menu}
'''


# note We need to organise the numbering of these two menus so as to follow the other nutrients on from the mandatory
# nutrients. That way, we can use the same validator for both, and we don't need sperate editor functions to edit
# items from each list.


class NutrientContentEditorComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self._subject: Optional['SupportsSettingNutrientContent'] = None
        self._return_to_route: Optional[str] = None
        self._backup_nutrients_data: Dict[str, 'NutrientData'] = {}
        self._mandatory_nuts_menu_data: Dict[int, str] = {}
        self._other_nuts_menu_data: Dict[int, str] = {}

        self.configure_state('main', self._print_main_menu, responders=[
            self.configure_responder(self._on_ok, args=[
                PrimaryArg('ok', has_value=False, markers=['-ok'])]),
            self.configure_responder(self._on_cancel, args=[
                PrimaryArg('cancel', has_value=False, markers=['-cancel'])]),
            self.configure_responder(self._on_edit_nutrient, args=[
                PrimaryArg('edit', has_value=True, markers=['-edit'], validators=[self._validate_nut_number])]),
            self.configure_responder(self._on_new_nutrient, args=[
                PrimaryArg('new', has_value=False, markers=['-new'])]),
            self.configure_responder(self._on_reset_nutrient, args=[
                PrimaryArg('reset', has_value=True, markers=['-reset'], validators=[self._validate_nut_number])])
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
                nut_name=self._mandatory_nuts_menu_data[num].replace('_', ' ')+':',
                summary=self._subject.summarise_nutrient(self._mandatory_nuts_menu_data[num])
            )
        return menu

    @property
    def _other_nuts_menu(self) -> str:
        if len(self._other_nuts_menu_data):
            menu = ''
            for num in self._other_nuts_menu_data:
                menu = menu + '{num}. {nut_name}\n'.format(
                    num=num, nut_name=self._other_nuts_menu_data[num].replace('_', ' '))
        else:
            menu = 'No other nutrients defined yet.'
        return menu

    def _validate_nut_number(self, nut_num: Any) -> int:
        try:
            nut_num = int(nut_num)
        except TypeError:
            raise ResponseValidationError('Please enter a valid nutrient number.')
        if nut_num not in self._mandatory_nuts_menu_data.keys() or nut_num not in self._other_nuts_menu_data.keys():
            raise ResponseValidationError('Please enter a valid nutrient number.')
        return nut_num

    def _print_main_menu(self) -> str:
        output = _main_menu_template.format(
            mandatory_nuts_menu=self._mandatory_nuts_menu,
            other_nuts_menu=self._other_nuts_menu
        )
        return self.app.get_component(StandardPageComponent).print(
            page_title="Nutrient Content Editor",
            page_content=output
        )

    def _on_ok(self) -> None:
        self.app.goto(self._return_to_route)

    def _on_cancel(self) -> None:
        self._subject.set_nutrients_data(self._backup_nutrients_data)
        self.app.goto(self._return_to_route)

    def _on_edit_nutrient(self) -> None:
        raise NotImplementedError

    def _on_new_nutrient(self) -> None:
        raise NotImplementedError

    def _on_reset_nutrient(self) -> None:
        raise NotImplementedError
