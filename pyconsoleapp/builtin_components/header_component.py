from pyconsoleapp import ConsoleAppComponent

class HeaderComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app)
        self.configure_printer(self.print_view)

    def print_view(self):
        output = ''
        output = output+self.app.fetch_component('title_bar_component').print()
        output = output + self.app.fetch_component('nav_options_component').print()
        output = output+self.app.fetch_component('single_hr_component').print()
        output = output + self.app.fetch_component('message_bar_component').print()
        return output
