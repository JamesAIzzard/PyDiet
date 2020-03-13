from pydiet.ingredients.ingredient import Ingredient
from pydiet.cli.main import app
from pydiet.utility_service import utility_service
from pydiet.data.repository_service import repo_service
from pydiet.ingredients.ingredient_service import ingredient_service

from pydiet.injector import injector

# Load the dependencies;
injector.utility_service = utility_service
injector.repo_service = repo_service
injector.ingredient_service = ingredient_service

# Run the UI;
app.run()
