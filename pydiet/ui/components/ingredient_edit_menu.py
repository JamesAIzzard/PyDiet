from pyconsoleapp.console_app_component import ConsoleAppComponent

_MENU_TEMPLATE = '''Choose an option:
1 -> {edit_or_new} ingredient name.
2 -> {edit_or_new} ingredient cost.
3 -> {edit_or_new} ingredient flags.
4 -> {edit_or_new} macronutrient totals.
5 -> {edit_or_new} macronutrients.
6 -> {edit_or_new} micronutrients.
7 -> {edit_or_new} all mandatory fields.
8 -> Save.
9 -> Cancel without saving.
'''

class IngredientEditMenu(ConsoleAppComponent):
    
    def get_screen(self):
        if 'edit' in self.app.route:
            return _MENU_TEMPLATE.format(edit_or_new='Edit')
        elif 'new' in self.app.route:
            return _MENU_TEMPLATE.format(edit_or_new='Enter')
        
    def on_edit_name(self):
        self.app.navigate(['home', 'ingredients', 'new', 'edit_name'])
        
ingredient_edit_menu = IngredientEditMenu()
ingredient_edit_menu.set_option_response('1', 'on_edit_name')