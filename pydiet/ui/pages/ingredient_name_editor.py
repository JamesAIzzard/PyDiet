from pyconsoleapp.console_app_page import ConsoleAppPage
from pyconsoleapp.components.header import header
from pydiet.ui.components.edit_ingredient_name import edit_ingredient_name as edit_ingredient_name_component

class IngredientNameEditor(ConsoleAppPage):
    pass

ingredient_name_editor = IngredientNameEditor()
ingredient_name_editor.add_component(header)
ingredient_name_editor.add_component(edit_ingredient_name_component)