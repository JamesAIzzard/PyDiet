import pinjector

from pydiet.shared import utility_service
from pydiet.data import repository_service
from pydiet.ingredients import ingredient_service
from pydiet.recipes import recipe_service
from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService
from pydiet.cli.recipes.recipe_edit_service import RecipeEditService
from pydiet.cli.shared import utility_service as cli_utility_service
from pydiet.shared import configs

# Load the dependencies;
pinjector.create_namespace('pydiet')
pinjector.create_namespace('pydiet.cli')
pinjector.register('pydiet', configs)
pinjector.register('pydiet', utility_service)
pinjector.register('pydiet', repository_service)
pinjector.register('pydiet', ingredient_service)
pinjector.register('pydiet', recipe_service)
pinjector.register('pydiet.cli', cli_utility_service, 'utility_service')
pinjector.register('pydiet.cli', IngredientEditService)
pinjector.register('pydiet.cli', RecipeEditService)