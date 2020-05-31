from typing import TYPE_CHECKING

import pyconsoleapp as capp

if TYPE_CHECKING:
    from pyconsoleapp import ConsoleApp

# Run startup checks on data integrity;
from pydiet.data import validate_ingredient_template

app:'ConsoleApp' = capp.ConsoleApp('PyDiet')
app.register_component_package('pydiet.cli')
app.register_component_package('pydiet.cli.ingredients')
app.register_component_package('pydiet.cli.recipes')
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
app.add_route('home.ingredients.delete.confirm', 'ConfirmIngredientDeleteComponent')
app.add_route('home.recipes', 'RecipeMenuComponent')
app.add_route('home.recipes.edit', 'RecipeEditMenuComponent')
app.add_route('home.recipes.edit.name', 'EditRecipeNameComponent')
app.add_route('home.recipes.edit.serve_times', 'RecipeServeTimeEditorComponent')
app.add_route('home.recipes.search', 'RecipeSearchComponent')
app.add_route('home.recipes.search_results', 'RecipeSearchResultsComponent')