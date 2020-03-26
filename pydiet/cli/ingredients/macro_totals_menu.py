from pyconsoleapp.console_app_component import ConsoleAppComponent

_MACRO_TOTAL_MENU = '''Choose a macronutrient total to edit:
{}
'''
_MACRO_TOTAL_MENU_ITEM = '({number}) - {macro_total_name}\n'

class MacroTotalsMenu(ConsoleAppComponent):

    def __init__(self):
        super().__init__()

    def print(self):
        scope = self.get_scope('ingredient_edit')
        totals_menu = ''
        for number in scope.nutrient_number_map.keys():
            totals_menu = totals_menu + _MACRO_TOTAL_MENU_ITEM.format(
                number = number,
                macro_total_name = scope.get_nutrient_name(\
                    number, scope).replace('_', ' ')
            )
        output = _MACRO_TOTAL_MENU.format(totals_menu)
        output = self.app.get_component('StandardPage').print(output)
        return output

    def dynamic_response(self, response):
        scope = self.get_scope('ingredient_edit')
        if response in scope.nutrient_number_map.keys():
            scope.nutrient_number = int(response)
        self.app.navigate(['.', 'sample_mass'])