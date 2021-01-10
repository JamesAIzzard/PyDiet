import pydiet
from pydiet import recipes


class RecipeMenuComponent(pydiet.cli_components.CRUDMenuComponent):

    def __init__(self, app):
        super().__init__(subject_type_name='recipe',
                         subject_type=recipes.Recipe,
                         new_subject_factory=recipes.get_new_recipe,
                         subject_editor_component=recipes.cli_components.RecipeEditorComponent,
                         subject_search_component=recipes.cli_components.RecipeSearchComponent,
                         subject_base_route='home.recipes', app=app)
