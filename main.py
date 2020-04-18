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
app.add_route('home.ingredients.new.edit_name', 'EditNameComponent')
app.add_route('home.ingredients.new.flags', 'EditFlagMenuComponent')
app.add_route('home.ingredients.new.flags.ask_cycle_flags', 'AskCycleFlagsComponent')
app.add_route('home.ingredients.new.flags.edit_flag', 'EditFlagComponent')
app.add_route('home.ingredients.new.flags.tell_flags_are_set', 'TellFlagsAreSetComponent')
app.add_route('home.ingredients.new.edit_cost_mass', 'EditCostMassComponent')
app.add_route('home.ingredients.new.edit_cost', 'EditCostComponent')
app.add_route('home.ingredients.new.edit_density_volume', 'EditDensityVolumeComponent')
app.add_route('home.ingredients.new.edit_density_mass', 'EditDensityMassComponent')
app.add_route('home.ingredients.new.nutrients', 'EditNutrientMenuComponent')
app.add_route('home.ingredients.new.nutrients.edit_nutrient_ingredient_mass', 'EditNutrientIngredientMassComponent')
app.add_route('home.ingredients.new.nutrients.edit_nutrient_mass', 'EditNutrientMassComponent')
app.add_route('home.ingredients.new.nutrients.nutrient_search', 'NutrientSearchComponent')
app.add_route('home.ingredients.new.nutrients.nutrient_search_results', 'NutrientSearchResultsComponent')
app.run()

