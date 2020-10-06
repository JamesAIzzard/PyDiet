import abc
from typing import TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent, PrimaryArg

if TYPE_CHECKING:
    from pyconsoleapp import ConsoleApp


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
        # Define the template;
        template = '''
        {message}
        Yes | -y, -yes
        No  | -n, -no
        '''

        # Fill the template and return;
        output = template.format(
            message=self.message
        )
        output = self.app.fetch_component(
            'standard_page_component').print(content=output)
        return output

    @abc.abstractmethod
    def _on_yes(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _on_no(self) -> None:
        raise NotImplementedError
