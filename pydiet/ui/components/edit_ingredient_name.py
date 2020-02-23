from pyconsoleapp.console_app_component import ConsoleAppComponent
from pydiet.injector import injector

_NEW_NAME_TEMPLATE = '''Enter ingredient name: '''
_UPDATE_NAME_TEMPLATE = '''Ingredient Name: [{name}] (Enter to leave unchanged.)
New ingredient name:'''

class EditIngredientName(ConsoleAppComponent):
    
    def get_screen(self):
        current_name = injector.ingredient_service.current_ingredient.name
        if current_name:
            return _UPDATE_NAME_TEMPLATE.format(name=current_name)
        else:
            return _NEW_NAME_TEMPLATE
        
    def dynamic_response(self, response):
        if response == '':
            self.app.info_message = 'Ingredient name not changed.'
            self.app.navigate_back()
        else:
            current_ingredient = injector.ingredient_service.current_ingredient
            current_ingredient.name = response
            self.app.set_window_text(current_ingredient.summary)
            self.app.navigate_back()
        
edit_ingredient_name = EditIngredientName()
