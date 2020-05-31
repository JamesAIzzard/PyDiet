from typing import TYPE_CHECKING

from pyconsoleapp.components import ConsoleAppComponent

if TYPE_CHECKING: 
    from pyconsoleapp.console_app import ConsoleApp

class NavOptionsComponent(ConsoleAppComponent):
    
    def __init__(self, app:'ConsoleApp'):
        super().__init__(app)
        self.set_option_response('b', self.on_back)
        self.set_option_response('q', self.on_quit)

    def print(self):
        output = '(b)ack | (q)uit\n'
        return output

    def on_back(self)->None:
        self.app.goto('..')

    def on_quit(self)->None:
        self.app.quit()