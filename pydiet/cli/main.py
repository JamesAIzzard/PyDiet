from pyconsoleapp.console_app import ConsoleApp
from pydiet.cli.components.ingredient_menu import IngredientMenu
from pydiet.cli.components.main_menu import MainMenu
from pydiet.cli.components.standard_page import StandardPage
from pydiet.cli.components.ingredient_edit_menu import IngredientEditMenu
from pydiet.cli.components.ingredient_name_editor import IngredientNameEditor
from pydiet.cli.components.ingredient_flag_editor import IngredientFlagEditor
from pydiet.cli.components.ingredient_save_check import IngredientSaveCheck
from pydiet.cli.components.ingredient_create_check import IngredientCreateCheck

app = ConsoleApp('PyDiet')

app.register_component(IngredientMenu)
app.register_component(MainMenu)
app.register_component(StandardPage)
app.register_component(IngredientEditMenu)
app.register_component(IngredientNameEditor)
app.register_component(IngredientFlagEditor)
app.register_component(IngredientSaveCheck)
app.register_component(IngredientCreateCheck)

app.add_root_route(['home'], 'MainMenu')
app.add_route(['home', 'ingredients'], 'IngredientMenu')
app.add_route(['home', 'ingredients', 'new'], 'IngredientEditMenu')
app.add_route(['home', 'ingredients', 'new', 'name'], 'IngredientNameEditor')
app.add_route(['home', 'ingredients', 'new', 'flags'], 'IngredientFlagEditor')