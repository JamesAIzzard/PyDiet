from pyconsoleapp import ConsoleAppComponent

from pydiet.recipes.exceptions import (
    RecipeNameUndefinedError
)
from pydiet.recipes import recipe_edit_service as res
from pydiet.recipes import recipe_service as rcs

_TEMPLATE = '''Recipe Editor:

(s) -- Save Changes

(1) -- Edit Name: {name}

(2) -- Edit Serve Times:
{serve_times}
(3) -- Edit Tags:
{tags}
(4) -- Edit Ingredients:
{ingredients}
(5) -- Edit Steps:
{steps}
'''


class RecipeEditMenuComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app)
        self._res = res.RecipeEditService()
        self.set_option_response('s', self.on_save)
        self.set_option_response('1', self.on_edit_name)
        self.set_option_response('2', self.on_edit_serve_times)
        self.set_option_response('3', self.on_edit_tags)

    def run(self):
        # If there is no recipe loaded;
        if not self._res.recipe:
            # Go back to the main recipe state;
            self.goto('home.recipes')

    def print(self):
        # Raise an exception if recipe has not been loaded;
        if not self._res.recipe:
            raise AttributeError
        # Build the template;
        output = _TEMPLATE.format(
            name=rcs.summarise_name(self._res.recipe),
            serve_times=rcs.summarise_serve_intervals(self._res.recipe),
            tags=rcs.summarise_tags(self._res.recipe),
            ingredients=rcs.summarise_ingredients(self._res.recipe),
            steps=rcs.summarise_steps(self._res.recipe)
        )
        output = self.app.fetch_component(
            'standard_page_component').print(output)
        # Return the view;
        return output

    @property
    def _check_name_defined(self) -> bool:
        if not self._res.recipe.name:
            self.app.error_message = 'Recipe name must be set first.'
            return False
        else:
            return True

    def on_save(self) -> None:
        # Try and save the recipe;
        try:
            self._res.save_changes()
        # Inform the user if it is unnamed;
        except RecipeNameUndefinedError:
            self.app.error_message = 'Cannot save an un-named recipe.'

    def on_edit_name(self) -> None:
        self.app.goto('home.recipes.edit.name')

    def on_edit_serve_times(self) -> None:
        if self._check_name_defined:
            self.app.goto('home.recipes.edit.serve_times')

    def on_edit_tags(self) -> None:
        if self._check_name_defined:
            self.app.goto('home.recipes.edit.tags')
