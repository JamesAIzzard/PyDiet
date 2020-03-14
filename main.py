from pydiet.injector import injector
from pydiet.utility_service import UtilityService
from pydiet.data.repository_service import RepoService
from pydiet.ingredients.ingredient_service import IngredientService

# Load the dependencies;
injector.register(UtilityService)
injector.register(RepoService)
injector.register(IngredientService)

# Load the CLI;
from pydiet.cli.main import app
# Run the CLI;
app.run()
