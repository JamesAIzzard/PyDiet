from pyconsoleapp.console_app_component import ConsoleAppComponent

_FLAG_MENU = '''Choose a flag to edit:
{}
'''
_FLAG_MENU_ITEM = '({flag_number}) - {flag}\n'

class IngredientFlagMenu(ConsoleAppComponent):

    def __init__(self):
        super().__init__()

    def print(self):
        scope = self.get_scope('ingredient_edit')
        flags_menu = ''
        for flag_number in scope.flag_number_map.keys():
            flags_menu = flags_menu + _FLAG_MENU_ITEM.format(
                flag_number = flag_number,
                flag = scope.get_flag_name(flag_number, scope).replace('_', ' ')
            )
        output = _FLAG_MENU.format(flags_menu)
        output = self.app.get_component('StandardPage').print(output)
        return output

    def dynamic_response(self, response):
        scope = self.get_scope('ingredient_edit')
        scope.cycling_flags = False
        if str(response) in scope.flag_number_map.keys():
            scope.current_flag_number = int(response)
        self.app.navigate(['.', 'set'])
