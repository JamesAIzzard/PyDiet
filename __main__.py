from pydiet.injector import injector
import pydiet.data.repository_service as repo_service
import pydiet.ingredients.ingredient_service as ingredient_service
import pydiet.utility_service as utility_service
from pydiet.ui.app import app

# Load dependencies;
injector.repo_service = repo_service
injector.ingredient_service = ingredient_service
injector.utility_service = utility_service
# Run the UI;
app.run()

