import pinjector
from pyconsoleapp import ConsoleApp

from pydiet.utility_service import UtilityService
from pydiet.data.repository_service import RepoService
from pydiet.ingredients.ingredient_service import IngredientService
from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService

# Load the dependencies;
pinjector.create_namespace('pydiet')
pinjector.register('pydiet', UtilityService)
pinjector.register('pydiet', RepoService)
pinjector.register('pydiet', IngredientService)
pinjector.register('pydiet', IngredientEditService)

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
app.add_route('home.ingredients.new.macro_totals', 'MacroTotalsMenuComponent')
app.add_route('home.ingredients.new.macro_totals.sample_mass', 'NutrientPerMassComponent')
app.add_route('home.ingredients.new.macro_totals.nutrient_mass', 'NutrientMassComponent')
app.run()

# Test space ------------------
# ut:'UtilityService' = inject('utility_service')
# print(ut.parse_mass_and_units('100.5g'))
