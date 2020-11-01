import abc

from pyconsoleapp import Component, PrimaryArg


class YesNoDialogComponent(Component, abc.ABC):
    _template = u'''{hr}
{message}
Yes \u2502 -y, -yes
No  \u2502 -n, -no
{hr}
'''

    def __init__(self, message: str, **kwds):
        super().__init__(**kwds)
        self._message: str = message
        self.configure(responders=[
            self.configure_responder(self._on_yes, args=[
                PrimaryArg(name='yes', accepts_value=False, markers=['-y', '-yes'])]),
            self.configure_responder(self._on_no, args=[
                PrimaryArg(name='no', accepts_value=False, markers=['-n', '-no'])])
        ])

    @property
    def message(self) -> str:
        return self._message

    def printer(self, **kwds) -> str:
        return self._template.format(
            hr="\u2501" * self.app.terminal_width,
            message=self.message
        )

    @abc.abstractmethod
    def _on_yes(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _on_no(self) -> None:
        raise NotImplementedError
