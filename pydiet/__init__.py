from typing import TYPE_CHECKING

from pyconsoleapp import ConsoleApp

if TYPE_CHECKING:
    from pyconsoleapp import ConsoleApp

# Run startup checks on data integrity;
from pydiet.ingredients import validate_ingredient_template

# Create the app instance;
app:'ConsoleApp' = ConsoleApp('PyDiet')

# Configure the app framework;
app.register_component_package('pydiet.cli_components')
app.register_component_package('pydiet.ingredients.cli_components')
app.register_component_package('pydiet.recipes.cli_components')
app.register_component_package('pydiet.optimisation.cli_components')
app.root_route('home', 'MainMenuComponent')
app.add_route('home.ingredients', 'IngredientMenuComponent')
app.add_route('home.ingredients.search', 'IngredientSearchComponent')
app.add_route('home.ingredients.search_results', 'IngredientSearchResultsComponent')
app.add_route('home.ingredients.ask_search', 'SearchIngredientsQuestionComponent')
app.add_route('home.ingredients.view_all', 'ViewAllIngredientsComponent')
app.add_route('home.ingredients.edit', 'IngredientEditMenuComponent')
app.add_route('home.ingredients.edit.name', 'EditIngredientNameComponent')
app.add_route('home.ingredients.edit.flags', 'EditIngredientFlagMenuComponent')
app.add_route('home.ingredients.edit.flags.ask_cycle_flags', 'AskCycleIngredientFlagsComponent')
app.add_route('home.ingredients.edit.flags.set_flag', 'EditIngredientFlagComponent')
app.add_route('home.ingredients.edit.cost_qty', 'EditIngredientCostQtyComponent')
app.add_route('home.ingredients.edit.cost', 'EditIngredientCostComponent')
app.add_route('home.ingredients.edit.density_volume', 'EditIngredientDensityVolumeComponent')
app.add_route('home.ingredients.edit.density_mass', 'EditIngredientDensityMassComponent')
app.add_route('home.ingredients.edit.set_density_question', 'EditIngredientDensityQuestionComponent')
app.add_route('home.ingredients.edit.nutrients', 'EditIngredientNutrientMenuComponent')
app.add_route('home.ingredients.edit.nutrients.nutrient_ingredient_qty', 'EditIngredientNutrientQtyComponent')
app.add_route('home.ingredients.edit.nutrients.nutrient_mass', 'EditIngredientNutrientMassComponent')
app.add_route('home.ingredients.edit.nutrients.search', 'IngredientNutrientSearchComponent')
app.add_route('home.ingredients.edit.nutrients.search_results', 'IngredientNutrientSearchResultsComponent')
app.add_route('home.ingredients.delete', 'IngredientEditMenuComponent')
app.add_route('home.ingredients.delete.search', 'IngredientSearchComponent')
app.add_route('home.ingredients.delete.search_results', 'IngredientSearchResultsComponent')
app.add_route('home.ingredients.delete.confirm', 'ConfirmIngredientDeleteComponent')
app.add_route('home.recipes', 'RecipeMenuComponent')
app.add_route('home.recipes.edit', 'RecipeEditMenuComponent')
app.add_route('home.recipes.edit.name', 'EditRecipeNameComponent')
app.add_route('home.recipes.edit.serve_times', 'RecipeServeTimeEditorComponent')
app.add_route('home.recipes.edit.serve_times.edit_interval', 'TimeIntervalEditorComponent')
app.add_route('home.recipes.edit.tags', 'RecipeTagEditorComponent')
app.add_route('home.recipes.edit.ingredients', 'RecipeIngredientEditMenu')
app.add_route('home.recipes.edit.ingredients.search', 'IngredientSearchComponent')
app.add_route('home.recipes.edit.ingredients.search_results', 'IngredientSearchResultsComponent')
app.add_route('home.recipes.edit.ingredients.set_ingredient_qty', 'EditIngredientQtyComponent')
app.add_route('home.recipes.edit.ingredients.set_ingredient_variations', 'EditIngredientVarComponent')
app.add_route('home.recipes.edit.steps', 'RecipeStepEditMenuComponent')
app.add_route('home.recipes.edit.steps.edit_step', 'RecipeStepEditorComponent')
app.add_route('home.recipes.search', 'RecipeSearchComponent')
app.add_route('home.recipes.search_results', 'RecipeSearchResultsComponent')
app.add_route('home.recipes.delete.search', 'RecipeSearchComponent')
app.add_route('home.recipes.delete.search_results', 'RecipeSearchResultsComponent')
app.add_route('home.recipes.delete.confirm', 'ConfirmRecipeDeleteComponent')
app.add_route('home.recipes.ask_search', 'SearchRecipesQuestionComponent')
app.add_route('home.recipes.view_all', 'ViewAllRecipesComponent')
app.add_route('home.goals', 'GoalMenuComponent')
app.add_route('home.goals.edit_day', 'DayGoalsEditorComponent')
app.add_route('home.goals.edit_day.edit_meal', 'MealGoalsEditorComponent')
app.add_route('home.goals.confirm_delete_day', 'ConfirmDayGoalsDeleteComponent')
app.add_route('home.goals.edit_globals', 'GlobalDayGoalsEditorComponent')
app.add_route('home.goals.edit_globals.edit_flags', 'FlagEditorComponent')