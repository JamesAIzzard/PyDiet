from pyconsoleapp.builtin_components.yes_no_dialog_component import YesNoDialogComponent


class EditIngredientDensityQuestionComponent(YesNoDialogComponent):
    def __init__(self):
        super().__init__()
        self.message = 'Volumetric measurements are not configured on {} yet. Would you like to configure them now?'

    def on_yes(self):
        self.app.goto('home.ingredients.edit.density_volume')

    def on_no(self):
        self.app.goto('home.ingredients.edit')
