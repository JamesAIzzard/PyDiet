import abc
from typing import TYPE_CHECKING

import pyconsoleapp as pcap
from pyconsoleapp import ConsoleAppComponent, PrimaryArg

if TYPE_CHECKING:
    from pyconsoleapp import ConsoleApp

_view_template = '''
{message}
Yes | -y, -yes
No  | -n, -no
'''


class YesNoDialogComponent(ConsoleAppComponent, abc.ABC):

    def __init__(self, message: str, app: 'ConsoleApp'):
        super().__init__(app)
        self._message: str = message
        self.configure_state('main', self._print_dialog, responders=[
            self.configure_responder(self._on_yes, args=[
                PrimaryArg('on_yes', has_value=False, markers=['-y', '-yes'])]),
            self.configure_responder(self._on_no, args=[
                PrimaryArg('on_no', has_value=False, markers=['-n', '-no'])])
        ])

    @property
    def message(self) -> str:
        return self._message

    def _print_dialog(self) -> str:
        return self.app.get_component(pcap.StandardPageComponent).print_view(
            page_content=_view_template.format(message=self.message)
        )

    @abc.abstractmethod
    def _on_yes(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _on_no(self) -> None:
        raise NotImplementedError
