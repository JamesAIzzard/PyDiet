from pinjector import register, inject
from pydiet.utility_service import UtilityService
from pydiet.data.repository_service import RepoService
from pydiet.ingredients.ingredient_service import IngredientService

# Load the dependencies;
register(UtilityService)
register(RepoService)
register(IngredientService)

# Load the  CLI;
from pydiet.cli.main import app

# Run the CLI;
app.run()

# Test space ------------------
# ut:'UtilityService' = inject('utility_service')
# print(ut.parse_mass_and_units('100.5g'))
