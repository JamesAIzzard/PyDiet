from typing import TYPE_CHECKING

from pyconsoleapp import styles
from pyconsoleapp.components import ConsoleAppComponent

if TYPE_CHECKING:
    from pyconsoleapp.console_app import ConsoleApp


class HeaderComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app)
        self.set_print_function(self.print)

    def print(self):
        output = ''
        output = output+self.app.fetch_component('title_bar_component').call_print()
        output = output + self.app.fetch_component('nav_options_component').call_print()
        output = output+self.app.fetch_component('single_hr_component').call_print()
        output = output + self.app.fetch_component('message_bar_component').call_print()
        return output
