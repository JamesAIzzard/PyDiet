from pydiet import recipes
from pydiet.cli_components.crud_menu_component import CRUDMenuComponent
from pydiet.recipes import cli_components as rcli


class RecipeMenuComponent(CRUDMenuComponent):

    def __init__(self, app):
        super().__init__(subject_type_name='recipe',
                         subject_type=recipes.Recipe,
                         new_subject_factory=recipes.get_new_recipe,
                         subject_editor_component=rcli.recipe_editor_component.RecipeEditorComponent,
                         subject_search_component=rcli.recipe_search_component.RecipeSearchComponent,
                         subject_base_route='home.recipes', app=app)
