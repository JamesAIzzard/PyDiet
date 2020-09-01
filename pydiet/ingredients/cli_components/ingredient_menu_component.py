from typing import TYPE_CHECKING, cast

from pyconsoleapp import ConsoleAppComponent

from pydiet.repository import repository_service
from pydiet.ingredients import ingredient_service

if TYPE_CHECKING:
    from pydiet.ingredients.cli_components.ingredient_editor_component import IngredientEditorComponent
    from pydiet.ingredients.cli_components.ingredient_search_component import IngredientSearchComponent

_menu_template = '''
Ingredient Count: {ingredient_count}
----------------------------|-------------
Create a New Ingredient     | -new
Edit an Ingredient          | -edit
Delete an Ingredient        | -del
View Ingredients            | -view
----------------------------|-------------
'''


class IngredientMenuComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app)
        self.configure_printer(self.print_menu_view)
        self.configure_responder(self.on_create, args=[
                                 self.configure_valueless_primary_arg('new', ['-new', '-n'])])
        self.configure_responder(self.on_edit, args=[
                                 self.configure_valueless_primary_arg('edit', ['-edit', '-e'])])
        self.configure_responder(self.on_delete, args=[
                                 self.configure_valueless_primary_arg('delete', ['-delete', '-d'])])
        self.configure_responder(self.on_view, args=[
                                 self.configure_valueless_primary_arg('view', ['-view', '-v'])])                                                                                                   

    def print_menu_view(self):
        # Calculate the ingredient count;
        ingredient_count = len(repository_service.read_ingredient_index())
        # Build the template
        output = _menu_template.format(
            ingredient_count=ingredient_count
        )
        # Frame and return the template;
        output = self.app.fetch_component(
            'standard_page_component').print(
                page_content=output,
                page_title='Ingredient Menu'
            )
        return output

    def on_create(self):
        # Place a new ingredient in the editor component;
        i = ingredient_service.load_new_ingredient()
        iec = self.app.fetch_component('ingredient_editor_component')
        iec = cast('IngredientEditorComponent', iec)
        iec.subject = i

        # Configure the save reminder;
        self.app.guard_exit('home.ingredients.edit',
                            'IngredientSaveCheckComponent')
        # Go;
        self.app.goto('home.ingredients.edit')

    def on_edit(self):
        # Configure the ingredient search component to locate
        # the ingredient to edit and load it into the editor;
        isc = self.app.fetch_component('ingredient_search_component')
        isc = cast('IngredientSearchComponent', isc)
        def on_ingredient_found():
            # Load the ingredient into the editor and open it;
            i = ingredient_service.load_ingredient(isc.datafile_name)
            iec = self.app.fetch_component('ingredient_editor_component')
            iec = cast('IngredientEditorComponent', iec)
            iec.subject = i
        isc.on_ingredient_found = on_ingredient_found 

        self.app.goto('home.ingredients.search')

    def on_delete(self):
        self.app.goto('home.ingredients.delete.search')

    def on_view(self):
        self.app.goto('home.ingredients.ask_search')
