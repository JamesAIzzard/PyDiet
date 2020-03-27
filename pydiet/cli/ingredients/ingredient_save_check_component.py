from pyconsoleapp.builtin_components.yes_no_dialog_component import YesNoDialogComponent

class IngredientSaveCheckComponent(YesNoDialogComponent):

    def __init__(self):
        super().__init__()
        self.set_option_response('y', self.on_yes_save)
        self.set_option_response('n', self.on_no_dont_save)
        self.message:str = 'Save changes to this ingredient?'
        self.guarded_route:str

    def on_yes_save(self):
        self.app.info_message = 'Ingredient saved.'
        self.app.clear_exit(self.guarded_route)      

    def on_no_dont_save(self):
        self.app.info_message = 'Ingredient not saved.'
        self.app.clear_exit(self.guarded_route)     