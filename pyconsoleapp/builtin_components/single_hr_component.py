from pyconsoleapp.console_app_component import ConsoleAppComponent
from pyconsoleapp import configs


class SingleHrComponent(ConsoleAppComponent):
    
    def print(self):
        output = '-'*configs.terminal_width_chars+'\n'
        return output
