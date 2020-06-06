from typing import TYPE_CHECKING

from pyconsoleapp import styles
from pyconsoleapp.components import ConsoleAppComponent

if TYPE_CHECKING:
    from pyconsoleapp.console_app import ConsoleApp


class TitleBarComponent(ConsoleAppComponent):
    def __init__(self, app: 'ConsoleApp'):
        super().__init__(app)

    def print(self):
        output = self.app.name+'\n'
        output = styles.weight(output, 'bright')
        return output
