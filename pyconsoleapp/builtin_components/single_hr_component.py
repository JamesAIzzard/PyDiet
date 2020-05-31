from typing import TYPE_CHECKING

from pyconsoleapp.components import ConsoleAppComponent
from pyconsoleapp import configs

if TYPE_CHECKING:
    from pyconsoleapp.console_app import ConsoleApp

class SingleHrComponent(ConsoleAppComponent):
    def __init__(self, app: 'ConsoleApp'):
        super().__init__(app)    
    def print(self):
        output = '-'*configs.terminal_width_chars+'\n'
        return output
