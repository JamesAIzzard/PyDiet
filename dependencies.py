import pinjector

from pydiet import utility_service
from pydiet.data import repository_service
from pydiet.ingredients import ingredient_service
from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService
from pydiet import configs

# Load the dependencies;
pinjector.create_namespace('pydiet')
pinjector.register('pydiet', utility_service)
pinjector.register('pydiet', repository_service)
pinjector.register('pydiet', ingredient_service)
pinjector.register('pydiet', IngredientEditService)
pinjector.register('pydiet', configs)