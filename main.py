import pinjector
from pyconsoleapp import ConsoleApp

from pydiet.utility_service import UtilityService
from pydiet.data import repository_service
from pydiet.ingredients import ingredient_service
from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService
from pydiet import configs

# Load the dependencies;
pinjector.create_namespace('pydiet')
pinjector.register('pydiet', UtilityService)
pinjector.register('pydiet', repository_service)
pinjector.register('pydiet', ingredient_service)
pinjector.register('pydiet', IngredientEditService)
pinjector.register('pydiet', configs)

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

# Test space ------------------
# ut:'UtilityService' = inject('utility_service')
# print(ut.parse_mass_and_units('100.5g'))
