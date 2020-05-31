from abc import abstractmethod
from typing import TYPE_CHECKING

from pyconsoleapp.components import ConsoleAppComponent
from pyconsoleapp import configs

if TYPE_CHECKING:
    from pyconsoleapp.console_app import ConsoleApp

_TEMPLATE = '''
{message}
{space}(y)es / (n)o?{space}
'''


class YesNoDialogComponent(ConsoleAppComponent):

    def __init__(self, app: 'ConsoleApp'):
        super().__init__(app)
        self.message: str
        self.set_option_response('y', self.on_yes)
        self.set_option_response('n', self.on_no)

    def print(self):
        output = _TEMPLATE.format(
            message=self.message,
            space=int((configs.terminal_width_chars-13)/2)*''
        )
        output = self.app.fetch_component(
            'standard_page_component').print(output)
        return output

    @abstractmethod
    def on_yes(self):
        pass

    @abstractmethod
    def on_no(self):
        pass
