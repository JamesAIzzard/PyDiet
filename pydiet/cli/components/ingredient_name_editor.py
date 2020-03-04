from pyconsoleapp.console_app_component import ConsoleAppComponent

_TEMPLATE = '''Enter ingredient name:
'''

class IngredientNameEditor(ConsoleAppComponent):

    def run(self):
        output = _TEMPLATE
        output = self.run_parent('standard_page', output)
        return output

    def dynamic_response(self, response):
        self.app.set_window_text(response)
        self.app.show_text_window()
        self.app.navigate_back()

ingredient_name_editor = IngredientNameEditor()