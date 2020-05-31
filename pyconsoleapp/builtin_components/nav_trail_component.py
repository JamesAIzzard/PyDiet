from typing import TYPE_CHECKING

from pyconsoleapp.components import ConsoleAppComponent

if TYPE_CHECKING:
    from pyconsoleapp.console_app import ConsoleApp


class NavTrailComponent(ConsoleAppComponent):
    
    def __init__(self, app: 'ConsoleApp'):
        super().__init__(app)

    def print(self):
        trail = self.app.route.replace('.', '>')
        return trail+'\n'
