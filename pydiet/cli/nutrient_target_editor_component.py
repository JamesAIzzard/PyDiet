from typing import Dict, cast, TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent, parse_tools

if TYPE_CHECKING:
    from pydiet.nutrient_targetable import NutrientTargetable
    from pydiet.cli_components.nutrient_search_component import NutrientSearchComponent

_EDIT_QTY_TEMPLATE = '''
Enter a the target quantity for {primary_nutrient_name}:
(e.g. 100g, 100mg etc.)
'''


class NutrientTargetEditorComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app)
        self.set_print_function(self.print_edit_template)
        self.set_any_response_function(self.on_edit_nutrient_qty)
        self.subject: 'NutrientTargetable'
        self.nutrient_name = []

    def on_run(self) -> None:
        # Redirect to nutrient search if no nutrient name;
        if self.nutrient_name == []:
            # Grab ref to search component;
            nsc = cast('NutrientSearchComponent',
                       self.app.fetch_component('nutrient_search_component'))
            # Set configure it;
            nsc.chosen_nutrient_name = self.nutrient_name
            nsc.return_route = self.app.route
            # Go to it;
            self.app.goto(
                'home.goals.edit_globals.edit_nutrient_targets.search_nutrient')

    def print_edit_template(self)->str:
        output = _EDIT_QTY_TEMPLATE.format(nutrient_name=self.nutrient_name[0])
        return self.app.fetch_component('standard_page_component').call_print(output)

    def on_edit_nutrient_qty(self, response:str)->None:
        # Try parse the qty and units;
        try:
            qty, units = parse_tools.parse_number_and_text(response)
        except parse_tools.NumberAndTextParseError:
            self.app.error_message = '{} could not be parsed as a qty and unit.'.format(response)
            return
        # Set the target;
        self.subject.add_nutrient_target(self.nutrient_name[0], qty, units)
        # Reset the nutrient name;
        self.nutrient_name = []
        # Redirect to edit globals;
        self.app.goto('home.goals.edit_globals')
