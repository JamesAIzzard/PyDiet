from pyconsoleapp.console_app import ConsoleApp
from pydiet.ui.pages.home import home as home_page
from pydiet.ui.pages.ingredient_menu import ingredient_menu as ingredient_menu_page
from pydiet.ui.pages.ingredient_editor import ingredient_editor as ingredient_editor_page
from pydiet.ui.pages.ingredient_name_editor import ingredient_name_editor as ingredient_name_editor_page

app = ConsoleApp('PyDiet')
app.add_route(['home'], home_page)
app.add_route(['home', 'ingredients'], ingredient_menu_page)
app.add_route(['home', 'ingredients', 'new'], ingredient_editor_page)
app.add_route(['home', 'ingredients', 'new', 'edit_name'], ingredient_name_editor_page)
app.add_route(['home', 'ingredients', 'edit'], ingredient_editor_page)
