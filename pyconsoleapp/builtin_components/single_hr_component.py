from pyconsoleapp import ConsoleAppComponent, configs

class SingleHrComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app) 
        self.set_print_function(self.print)

    def print(self):
        output = '-'*configs.terminal_width_chars+'\n'
        return output
