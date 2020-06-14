from pyconsoleapp.builtin_components.yes_no_dialog_component import YesNoDialogComponent

class SearchRecipesQuestionComponent(YesNoDialogComponent):
    def __init__(self, app):
        super().__init__(app)
        self.message = 'Search for a particular recipe?'

    def on_yes(self):
        self.app.goto('home.recipes.search')

    def on_no(self):
        self.app.goto('home.recipes.view_all')