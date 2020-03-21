from pyconsoleapp.builtin_components.yes_no_dialog import YesNoDialog

class IngredientSaveCheck(YesNoDialog):

    def __init__(self):
        super().__init__()
        self.set_option_response('y', self.on_yes_save)
        self.set_option_response('n', self.on_no_dont_save)
        self.message = 'Save changes to this ingredient?'
        self.guard_route = ['home', 'ingredients', 'new']

    def on_yes_save(self):
        self.app.info_message = 'Ingredient saved.'
        self.app.clear_exit(self.guard_route)      

    def on_no_dont_save(self):
        self.app.info_message = 'Ingredient not saved.'
        self.app.clear_exit(self.guard_route)     