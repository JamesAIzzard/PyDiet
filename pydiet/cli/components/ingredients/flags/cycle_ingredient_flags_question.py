from pyconsoleapp.console_app_component import ConsoleAppComponent

_TEMPLATE = '\nSet all flags now? (y)/(n)\n\n'

class CycleIngredientFlagsQuestion(ConsoleAppComponent):
    def __init__(self):
        super().__init__()
        self.set_option_response('y', self.on_yes_set_all)
        self.set_option_response('n', self.on_no_dont_set_all)

    def print(self):
        output = _TEMPLATE
        output = self.app.get_component('StandardPage').print(output)
        return output

    def on_yes_set_all(self):
        scope = self.get_scope('ingredient_edit')
        scope.current_flag_number = 1
        scope.cycling_flags = True
        self.app.navigate_back()
        self.app.navigate(['.', 'set'])

    def on_no_dont_set_all(self):
        self.app.navigate(['home', 'ingredients', 'new', 'flags'])
