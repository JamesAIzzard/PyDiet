from pyconsoleapp import ConsoleAppComponent

_TEMPLATE = '''
Search for a particular ingredient?

    (y)es/(n)o

'''

class SearchIngredientsQuestionComponent(ConsoleAppComponent):
    def __init__(self):
        super().__init__()
        self.set_option_response('y', self.on_yes)
        self.set_option_response('n', self.on_no)

    def print(self):
        output = _TEMPLATE
        output = self.get_component('standard_page_component').print(output)
        return output

    def on_yes(self):
        self.goto('.search')

    def on_no(self):
        self.goto('.view_all')