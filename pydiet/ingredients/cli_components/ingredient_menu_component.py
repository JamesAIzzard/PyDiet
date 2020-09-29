from typing import TYPE_CHECKING, cast

from pyconsoleapp import ConsoleAppComponent, styles, PrimaryArg
from pydiet import ingredients, persistence

if TYPE_CHECKING:
    from pydiet.ingredients.cli_components.ingredient_editor_component import IngredientEditorComponent

_menu_screen_template = '''
Ingredient Count: {ingredient_count}

Create a New Ingredient | -new
Edit an Ingredient      | -edit
Delete an Ingredient    | -del
View Ingredients        | -view

'''


class IngredientMenuComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app)
        self.configure_state('menu', self._print_menu_screen, responders=[
            self.configure_responder(self._on_create, args=[
                PrimaryArg('new', has_value=False, markers=['-new'])]),
            self.configure_responder(self._on_edit, args=[
                PrimaryArg('edit', has_value=False, markers=['-edit'])]),
            self.configure_responder(self._on_view, args=[
                PrimaryArg('view', has_value=False, markers=['-view'])])
        ])

    def _print_menu_screen(self):
        # Calculate the ingredient count;
        ingredient_count = persistence.persistence_service.count_saved_instances(
            ingredients.ingredient.Ingredient
        )
        # Build the template
        output = _menu_screen_template.format(
            ingredient_count=styles.fore(ingredient_count, 'blue')
        )
        # Frame and return the template;
        output = self.app.fetch_component(
            'standard_page_component').print(
            page_content=output,
            page_title='Ingredient Menu'
        )
        return output

    def _on_create(self):
        # Place a new ingredient in the editor component;
        i = ingredients.ingredient_service.load_new_ingredient()
        iec = self.app.fetch_component('ingredient_editor_component')
        iec = cast('IngredientEditorComponent', iec)
        iec._subject = i

        # Configure the save reminder;
        self.app.guard_exit('home.ingredients.edit',
                            'IngredientSaveCheckComponent')
        # Go;
        self.app.goto('home.ingredients.edit')

    def _on_edit(self) -> None:
        isc = self.app.get_component(ingredients.cli_components.ingredient_search_component.IngredientSearchComponent)

        def on_result_selected(ingredient_name: str):
            iec = self.app.get_component(
                ingredients.cli_components.ingredient_editor_component.IngredientEditorComponent)
            selected_ingredient = persistence.persistence_service.load(
                ingredients.ingredient.Ingredient, ingredient_name)
            iec.configure(ingredient=selected_ingredient)
            self.app.goto('home.ingredients.edit')

        isc.configure(subject_name='Ingredient', on_result_selected=on_result_selected)
        self.app.goto('home.ingredients.search')

    def _on_view(self) -> None:
        self.app.goto('home.ingredients.view')