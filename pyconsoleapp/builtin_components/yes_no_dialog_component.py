from abc import abstractmethod
from typing import TYPE_CHECKING

from pyconsoleapp.components import ConsoleAppComponent
from pyconsoleapp import configs

if TYPE_CHECKING:
    from pyconsoleapp.console_app import ConsoleApp

_TEMPLATE = '''
{message}
-yes, -y    -> Yes
-no, -n     -> No
'''


class YesNoDialogComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app)
        self.message: str
        self.set_print_function(self.print)
        self.set_response_function(['-yes', '-y'], self.on_yes)
        self.set_response_function(['-no', '-n'], self.on_no)

    def print(self):
        output = _TEMPLATE.format(
            message=self.message
        )
        output = self.app.fetch_component(
            'standard_page_component').call_print(content=output)
        return output

    @abstractmethod
    def on_yes(self):
        pass

    @abstractmethod
    def on_no(self):
        pass
