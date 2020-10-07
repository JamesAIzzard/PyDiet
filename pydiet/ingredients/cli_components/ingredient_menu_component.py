from pydiet import ingredients
from pydiet.cli_components.crud_menu_component import CRUDMenuComponent
from pydiet.ingredients import cli_components as icli


class IngredientMenuComponent(CRUDMenuComponent):

    def __init__(self, app):
        super().__init__(subject_type_name='ingredient',
                         subject_type=ingredients.ingredient.Ingredient,
                         new_subject_factory=ingredients.ingredient.load_new_ingredient,
                         subject_editor_component=icli.ingredient_editor_component.IngredientEditorComponent,
                         subject_search_component=icli.ingredient_search_component.IngredientSearchComponent,
                         subject_base_route='home.ingredients', app=app)
