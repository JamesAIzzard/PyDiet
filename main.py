import pinjector
from pyconsoleapp import ConsoleApp

import dependencies

# Run startup checks on data integrity;
from pydiet.data import validate_ingredient_template

# Configure the cli;
app:'ConsoleApp' = ConsoleApp('PyDiet')
pinjector.register('pydiet.cli', app, 'app')
app.register_component_package('pydiet.cli')
app.register_component_package('pydiet.cli.ingredients')
app.register_component_package('pydiet.cli.recipes')
app.root_route('home', 'MainMenuComponent')
app.add_route('home.ingredients', 'IngredientMenuComponent')
app.add_route('home.ingredients.new', 'IngredientEditMenuComponent')
app.add_route('home.ingredients.new.edit_name', 'EditNameComponent')
app.add_route('home.ingredients.new.flags', 'EditFlagMenuComponent')
app.add_route('home.ingredients.new.flags.ask_cycle_flags', 'AskCycleFlagsComponent')
app.add_route('home.ingredients.new.flags.edit_flag', 'EditFlagComponent')
app.add_route('home.ingredients.new.flags.tell_flags_are_set', 'TellFlagsAreSetComponent')
app.add_route('home.ingredients.new.edit_cost_qty', 'EditCostQtyComponent')
app.add_route('home.ingredients.new.edit_cost', 'EditCostComponent')
app.add_route('home.ingredients.new.edit_density_volume', 'EditDensityVolumeComponent')
app.add_route('home.ingredients.new.edit_density_mass', 'EditDensityMassComponent')
app.add_route('home.ingredients.new.edit_density_question', 'EditDensityQuestionComponent')
app.add_route('home.ingredients.new.nutrients', 'EditNutrientMenuComponent')
app.add_route('home.ingredients.new.nutrients.edit_nutrient_ingredient_qty', 'EditNutrientIngredientQtyComponent')
app.add_route('home.ingredients.new.nutrients.edit_nutrient_mass', 'EditNutrientMassComponent')
app.add_route('home.ingredients.new.nutrients.nutrient_search', 'NutrientSearchComponent')
app.add_route('home.ingredients.new.nutrients.nutrient_search_results', 'NutrientSearchResultsComponent')
app.add_route('home.ingredients.edit', 'IngredientEditMenuComponent')
app.add_route('home.ingredients.edit.search', 'IngredientSearchComponent')
app.add_route('home.ingredients.edit.search_results', 'IngredientSearchResultsComponent')
app.add_route('home.ingredients.edit.edit_name', 'EditNameComponent')
app.add_route('home.ingredients.edit.flags', 'EditFlagMenuComponent')
app.add_route('home.ingredients.edit.flags.ask_cycle_flags', 'AskCycleFlagsComponent')
app.add_route('home.ingredients.edit.flags.edit_flag', 'EditFlagComponent')
app.add_route('home.ingredients.edit.flags.tell_flags_are_set', 'TellFlagsAreSetComponent')
app.add_route('home.ingredients.edit.edit_cost_qty', 'EditCostQtyComponent')
app.add_route('home.ingredients.edit.edit_cost', 'EditCostComponent')
app.add_route('home.ingredients.edit.edit_density_volume', 'EditDensityVolumeComponent')
app.add_route('home.ingredients.edit.edit_density_mass', 'EditDensityMassComponent')
app.add_route('home.ingredients.edit.edit_density_question', 'EditDensityQuestionComponent')
app.add_route('home.ingredients.edit.nutrients', 'EditNutrientMenuComponent')
app.add_route('home.ingredients.edit.nutrients.edit_nutrient_ingredient_qty', 'EditNutrientIngredientQtyComponent')
app.add_route('home.ingredients.edit.nutrients.edit_nutrient_mass', 'EditNutrientMassComponent')
app.add_route('home.ingredients.edit.nutrients.nutrient_search', 'NutrientSearchComponent')
app.add_route('home.ingredients.edit.nutrients.nutrient_search_results', 'NutrientSearchResultsComponent')
app.add_route('home.ingredients.delete', 'IngredientEditMenuComponent')
app.add_route('home.ingredients.delete.search', 'IngredientSearchComponent')
app.add_route('home.ingredients.delete.search_results', 'IngredientSearchResultsComponent')
app.add_route('home.ingredients.delete.confirm', 'ConfirmIngredientDeleteComponent')
app.add_route('home.ingredients.view', 'SearchIngredientsQuestionComponent')
app.add_route('home.ingredients.view.search', 'IngredientSearchComponent')
app.add_route('home.ingredients.view.search_results', 'IngredientSearchResultsComponent')
app.add_route('home.ingredients.view.view_all', 'ViewAllIngredientsComponent')

# Run the cli;
app.run()

