from pyconsoleapp import ConsoleAppComponent

_FLAGS_SET_CONFIRMATION = '''\nAll flags are set!
        (o)k.\n
'''

class TellIngredientFlagsAreSetComponent(ConsoleAppComponent):
    def __init__(self):
        super().__init__()
        self.set_option_response('o', self.on_ok)

    def print(self):
        output = _FLAGS_SET_CONFIRMATION
        output = self.app.fetch_component('standard_page_component').print(output)
        return output

    def on_ok(self):
        self.app.goto('...')