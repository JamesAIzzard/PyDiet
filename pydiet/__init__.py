from pyconsoleapp import ConsoleApp

from .core import flag_nutrient_relations, nutrient_flag_relations
from .flag_nutrient_relation import FlagNutrientRelation

from pydiet import cli, configs, exceptions
from pydiet.name import HasName, HasSettableName

app: 'ConsoleApp' = ConsoleApp('PyDiet')

app.configure(routes={
    "home": cli.MainMenuComponent,
    "home.ingredients": cli.IngredientMenuComponent,
    "home.ingredients.edit": cli.IngredientEditorComponent,
    "home.ingredients.view": cli.IngredientViewerComponent,
    "home.recipes": cli.RecipeMenuComponent,
    "home.recipes.edit": cli.RecipeEditorComponent,
    "home.recipes.view": cli.RecipeViewerComponent
})

app.current_route = 'home'
