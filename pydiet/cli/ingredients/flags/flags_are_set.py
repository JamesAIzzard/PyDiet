from pyconsoleapp import ConsoleAppComponent

_FLAGS_SET_CONFIRMATION = '''\nAll flags are set!
        (o)k.\n
'''

class FlagsAreSet(ConsoleAppComponent):
    def __init__(self):
        super().__init__()
        self.set_option_response('o', self.on_ok)

    def print(self):
        output = _FLAGS_SET_CONFIRMATION
        output = self.app.get_component('StandardPage').print(output)
        return output

    def on_ok(self):
        self.app.navigate_back()
        self.app.navigate_back()