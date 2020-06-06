from typing import TYPE_CHECKING

from pyconsoleapp import styles
from pyconsoleapp.components import ConsoleAppComponent

if TYPE_CHECKING:
    from pyconsoleapp.console_app import ConsoleApp


class HeaderComponent(ConsoleAppComponent):

    def __init__(self, app: 'ConsoleApp'):
        super().__init__(app)

    def print(self):
        output = ''
        output = output+self.app.fetch_component('title_bar_component').print()
        output = output+styles.weight(self.app.fetch_component('double_hr_component').print(), 'bright')
        output = output + \
            styles.weight(self.app.fetch_component('nav_options_component').print(), 'bright')
        output = output+styles.fore(self.app.fetch_component('nav_trail_component').print(), 'yellow')
        output = output+styles.weight(self.app.fetch_component('double_hr_component').print(), 'bright')
        output = output + \
            self.app.fetch_component('message_bar_component').print()
        return output
