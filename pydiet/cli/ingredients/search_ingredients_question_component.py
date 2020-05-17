from pyconsoleapp.builtin_components.yes_no_dialog_component import YesNoDialogComponent

class SearchIngredientsQuestionComponent(YesNoDialogComponent):
    def __init__(self):
        super().__init__()
        self.message = 'Search for a particular ingredient?'

    def on_yes(self):
        self.app.goto('home.ingredients.search')

    def on_no(self):
        self.app.goto('home.ingredients.view_all')