from pydiet import recipes
from pydiet.cli_components.crud_menu_component import CRUDMenuComponent
from pydiet.recipes import cli_components as rcli


class RecipeMenuComponent(CRUDMenuComponent):

    def __init__(self, app):
        super().__init__(app)
        super().configure(subject_type_name='recipe', subject_type=recipes.old_recipe.Recipe,
                          new_subject_factory=recipes.old_recipe.load_new_recipe,
                          subject_editor_component=rcli.recipe_editor_component.RecipeEditorComponent,
                          subject_search_component=rcli.recipe_search_component.RecipeSearchComponent,
                          subject_base_route='home.recipes')
