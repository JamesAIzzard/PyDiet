from pyconsoleapp.components.yes_no_dialog import YesNoDialog

class IngredientCreateCheck(YesNoDialog):

    def __init__(self):
        super().__init__()
        self.data['message'] = 'Do you really want to create a new ingredient?'

    def on_yes_create(self):
        self.app.navigate(['.', 'new'])
        self.app.clear_entrance(['home', 'ingredients', 'new'])

    def on_no_dont_create(self):
        self.app.navigate_back()

ingredient_create_check = IngredientCreateCheck()
ingredient_create_check.set_option_response('y', 'on_yes_create')
ingredient_create_check.set_option_response('n', 'on_no_dont_create')