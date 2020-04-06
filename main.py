import pinjector
from pyconsoleapp import ConsoleApp

import dependencies

# Configure & run the CLI
app:'ConsoleApp' = ConsoleApp('PyDiet')
pinjector.register('pydiet', app, 'app')
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
app.add_route('home.ingredients.new.macronutrient_totals', 'NutrientGroupEditMenuComponent')
app.add_route('home.ingredients.new.macronutrient_totals.sample_mass', 'NutrientPerMassComponent')
app.add_route('home.ingredients.new.macronutrient_totals.nutrient_mass', 'NutrientMassComponent')
app.add_route('home.ingredients.new.macronutrients', 'NutrientGroupEditMenuComponent')
app.add_route('home.ingredients.new.macronutrients.sample_mass', 'NutrientPerMassComponent')
app.add_route('home.ingredients.new.macronutrients.nutrient_mass', 'NutrientMassComponent')
app.add_route('home.ingredients.new.micronutrients', 'NutrientGroupEditMenuComponent')
app.add_route('home.ingredients.new.micronutrients.sample_mass', 'NutrientPerMassComponent')
app.add_route('home.ingredients.new.micronutrients.nutrient_mass', 'NutrientMassComponent')
app.run()

