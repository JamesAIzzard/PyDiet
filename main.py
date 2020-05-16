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
app.add_route('home.ingredients.new.edit_name', 'EditIngredientNameComponent')
app.add_route('home.ingredients.new.flags', 'EditIngredientFlagMenuComponent')
app.add_route('home.ingredients.new.flags.ask_cycle_flags', 'AskCycleIngredientFlagsComponent')
app.add_route('home.ingredients.new.flags.edit_flag', 'EditIngredientFlagComponent')
app.add_route('home.ingredients.new.flags.tell_flags_are_set', 'TellIngredientFlagsAreSetComponent')
app.add_route('home.ingredients.new.edit_cost_qty', 'EditIngredientCostQtyComponent')
app.add_route('home.ingredients.new.edit_cost', 'EditIngredientCostComponent')
app.add_route('home.ingredients.new.edit_density_volume', 'EditIngredientDensityVolumeComponent')
app.add_route('home.ingredients.new.edit_density_mass', 'EditIngredientDensityMassComponent')
app.add_route('home.ingredients.new.edit_density_question', 'EditIngredientDensityQuestionComponent')
app.add_route('home.ingredients.new.nutrients', 'EditIngredientNutrientMenuComponent')
app.add_route('home.ingredients.new.nutrients.edit_nutrient_ingredient_qty', 'EditIngredientNutrientQtyComponent')
app.add_route('home.ingredients.new.nutrients.edit_nutrient_mass', 'EditIngredientNutrientMassComponent')
app.add_route('home.ingredients.new.nutrients.nutrient_search', 'IngredientNutrientSearchComponent')
app.add_route('home.ingredients.new.nutrients.nutrient_search_results', 'IngredientNutrientSearchResultsComponent')
app.add_route('home.ingredients.edit', 'IngredientEditMenuComponent')
app.add_route('home.ingredients.edit.search', 'IngredientSearchComponent')
app.add_route('home.ingredients.edit.search_results', 'IngredientSearchResultsComponent')
app.add_route('home.ingredients.edit.edit_name', 'EditIngredientNameComponent')
app.add_route('home.ingredients.edit.flags', 'EditIngredientFlagMenuComponent')
app.add_route('home.ingredients.edit.flags.ask_cycle_flags', 'AskCycleIngredientFlagsComponent')
app.add_route('home.ingredients.edit.flags.edit_flag', 'EditIngredientFlagComponent')
app.add_route('home.ingredients.edit.flags.tell_flags_are_set', 'TellIngredientFlagsAreSetComponent')
app.add_route('home.ingredients.edit.edit_cost_qty', 'EditIngredientCostQtyComponent')
app.add_route('home.ingredients.edit.edit_cost', 'EditIngredientCostComponent')
app.add_route('home.ingredients.edit.edit_density_volume', 'EditIngredientDensityVolumeComponent')
app.add_route('home.ingredients.edit.edit_density_mass', 'EditIngredientDensityMassComponent')
app.add_route('home.ingredients.edit.edit_density_question', 'EditIngredientDensityQuestionComponent')
app.add_route('home.ingredients.edit.nutrients', 'EditIngredientNutrientMenuComponent')
app.add_route('home.ingredients.edit.nutrients.edit_nutrient_ingredient_qty', 'EditIngredientNutrientQtyComponent')
app.add_route('home.ingredients.edit.nutrients.edit_nutrient_mass', 'EditIngredientNutrientMassComponent')
app.add_route('home.ingredients.edit.nutrients.nutrient_search', 'IngredientNutrientSearchComponent')
app.add_route('home.ingredients.edit.nutrients.nutrient_search_results', 'IngredientNutrientSearchResultsComponent')
app.add_route('home.ingredients.delete', 'IngredientEditMenuComponent')
app.add_route('home.ingredients.delete.search', 'IngredientSearchComponent')
app.add_route('home.ingredients.delete.search_results', 'IngredientSearchResultsComponent')
app.add_route('home.ingredients.delete.confirm', 'ConfirmIngredientDeleteComponent')
app.add_route('home.ingredients.view', 'SearchIngredientsQuestionComponent')
app.add_route('home.ingredients.view.search', 'IngredientSearchComponent')
app.add_route('home.ingredients.view.search_results', 'IngredientSearchResultsComponent')
app.add_route('home.ingredients.view.view_all', 'ViewAllIngredientsComponent')
#
app.add_route('home.recipes', 'RecipeMenuComponent')
app.add_route('home.recipes.edit', 'RecipeEditMenuComponent')
app.add_route('home.recipes.edit.edit_name', 'EditRecipeNameComponent')
app.add_route('home.recipes.search', 'RecipeSearchComponent')
app.add_route('home.recipes.search_results', 'RecipeSearchResultsComponent')

# Run the cli;
app.run()

