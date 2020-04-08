import pinjector
from pyconsoleapp import ConsoleApp

import dependencies

# Configure & run the CLI
app:'ConsoleApp' = ConsoleApp('PyDiet')
pinjector.register('pydiet.cli', app, 'app')
app.register_component_package('pydiet.cli')
app.register_component_package('pydiet.cli.ingredients')
app.root_route('home', 'MainMenuComponent')
app.add_route('home.ingredients', 'IngredientMenuComponent')
app.add_route('home.ingredients.new', 'IngredientEditMenuComponent')
app.add_route('home.ingredients.new.name', 'IngredientNameEditorComponent')
app.add_route('home.ingredients.new.flags', 'IngredientFlagMenuComponent')
app.add_route('home.ingredients.new.flags.set_all?', 'CycleIngredientFlagsQuestionComponent')
app.add_route('home.ingredients.new.flags.set', 'SetFlagComponent')
app.add_route('home.ingredients.new.flags.flags_are_set', 'FlagsAreSetComponent')
app.add_route('home.ingredients.new.cost_mass', 'SetCostMassComponent')
app.add_route('home.ingredients.new.cost', 'SetCostComponent')
app.add_route('home.ingredients.new.nutrient_search', 'NutrientSearchComponent')
app.add_route('home.ingredients.new.nutrient_select', 'NutrientSelectComponent')
app.run()

