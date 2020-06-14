from pyconsoleapp.builtin_components.yes_no_dialog_component import YesNoDialogComponent

from pydiet.recipes import recipe_edit_service as res
from pydiet import repository_service as rep


class ConfirmRecipeDeleteComponent(YesNoDialogComponent):

    def __init__(self, app):
        super().__init__(app)
        self._res = res.RecipeEditService()
        self.message = 'Are you sure you want to delete {recipe_name}'.format(
            recipe_name=self._res.recipe.name)

    def on_yes(self):
        # If no datafile;
        if not self._res.datafile_name:
            raise AttributeError
        # Delete the datafile;
        rep.delete_recipe_data(self._res.datafile_name)
        # Set status message;
        self.app.info_message = '{recipe_name} deleted.'.format(recipe_name=self._res.recipe.name)
        # Redirect;
        self.app.goto('home.recipes')

    def on_no(self):
        self.app.info_message = 'Recipe was not deleted.'
        self.app.goto('home.recipes')