from typing import TYPE_CHECKING
from textwrap import fill

from pyconsoleapp.components import ConsoleAppComponent
from pyconsoleapp import configs, styles

if TYPE_CHECKING:
    from pyconsoleapp.console_app import ConsoleApp


class MessageBarComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self.set_print_function(self.print)

    def print(self):
        output = ''
        if self.app.error_message:
            output = output+'/!\\ Error:\n{}\n'.format(
                fill(self.app.error_message, configs.terminal_width_chars)
            )
            output = styles.fore(output, 'red')
            output = output+('-'*configs.terminal_width_chars)+'\n'
            self.app.error_message = None
        if self.app.info_message:
            output = output+'[i] Info:\n{}\n'.format(
                fill(self.app.info_message, configs.terminal_width_chars)
            )
            output = styles.fore(output, 'blue')
            output = output+self.app.fetch_component('single_hr_component').call_print()
            self.app.info_message = None
        return output
