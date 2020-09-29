from pyconsoleapp import ConsoleApp

# Expose internal modules
from . import exceptions, configs
from .exceptions import PyDietException

# Create the app instance;
app: 'ConsoleApp' = ConsoleApp('PyDiet')

# Configure the app framework;
app.register_component_packages([
    'pydiet.cli_components',
    'pydiet.cost.cli_components',
    'pydiet.flags.cli_components',
    'pydiet.goals.cli_components',
    'pydiet.ingredients.cli_components',
    'pydiet.nutrients.cli_components',
    'pydiet.quantity.cli_components',
    'pydiet.recipes.cli_components',
    'pydiet.tags.cli_components',
    'pydiet.time.cli_components',
])
app.root_route('home', 'MainMenuComponent')
app.add_route('home.ingredients', 'IngredientMenuComponent')
app.add_route('home.ingredients.search', 'IngredientSearchComponent')
app.add_route('home.ingredients.edit', 'IngredientEditorComponent')
app.add_route('home.ingredients.edit.flags', 'FlagEditorComponent')
app.add_route('home.ingredients.edit.bulk', 'BulkEditorComponent')
app.add_route('home.ingredients.edit.nutrients', 'NutrientContentEditorComponent')
app.add_route('home.ingredients.edit.nutrients.search', 'NutrientSearchComponent')
app.add_route('home.ingredients.view', 'IngredientViewerComponent')
