from pyconsoleapp.console_app_page import ConsoleAppPage
from pyconsoleapp.components.header import header
from pydiet.ui.components.ingredient_edit_menu import ingredient_edit_menu as ingredient_edit_menu_component

class IngredientEditor(ConsoleAppPage):
    pass

ingredient_editor = IngredientEditor()
ingredient_editor.add_component(header)
ingredient_editor.add_component(ingredient_edit_menu_component)