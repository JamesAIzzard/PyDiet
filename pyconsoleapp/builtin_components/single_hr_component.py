from pyconsoleapp import ConsoleAppComponent, configs

class SingleHrComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app) 
        self.configure_printer(self.print_view)

    def print_view(self):
        output = '-'*configs.terminal_width_chars+'\n'
        return output
