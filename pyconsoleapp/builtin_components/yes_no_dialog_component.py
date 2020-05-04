from pyconsoleapp.console_app_component import ConsoleAppComponent
from pyconsoleapp import configs

from typing import Optional

_TEMPLATE = '''
{message}
{space}(y)es / (n)o?{space}
'''

class YesNoDialogComponent(ConsoleAppComponent):

    def __init__(self):
        super().__init__()
        self.message:Optional[str] = None

    def print(self):
        output = _TEMPLATE.format(
            message = self.message,
            space = int((configs.terminal_width_chars-13)/2)*''
        )
        output = self.get_component('standard_page_component').print(output)
        return output
