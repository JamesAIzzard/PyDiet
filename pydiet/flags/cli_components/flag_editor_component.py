from typing import Dict, Optional, Any, TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent, Responder, PrimaryArg, ResponseValidationError, menu_tools, styles

if TYPE_CHECKING:
    from pydiet.flags.supports_flags import SupportsFlagSetting

_main_menu_template = '''
----------------|-------------------
OK              | -ok
Cancel          | -cancel
----------------|-------------------
Mark Flag Yes   | -yes [flag number]
Mark Flag No    | -no  [flag number]
Unset Flag      | -del [flag number]
----------------|-------------------

Flags:
{flag_menu}
'''


class FlagEditorComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self._subject: Optional['SupportsFlagSetting'] = None
        self._return_to_route: Optional[str] = None
        self._backup_flag_data: Dict[str, Optional[bool]] = {}
        self._flag_numbering: Dict[int, str] = {}

        self.configure_state('main', responders=[
            Responder(self.on_ok, args=[PrimaryArg('ok', has_value=False, markers=['-ok'])]),
            Responder(self.on_cancel, args=[PrimaryArg('cancel', markers=['cancel'])]),
            Responder(self.on_set_yes, args=[
                PrimaryArg('flag_num', has_value=True, markers=['-yes'], validators=[self._validate_flag_num])]),
            Responder(self.on_set_no, args=[
                PrimaryArg('flag_num', has_value=True, markers=['-no'], validators=[self._validate_flag_num])]),
            Responder(self.on_unset, args=[
                PrimaryArg('flag_num', has_value=True, markers=['-del'], validators=[self._validate_flag_num])
            ])
        ])

    def before_print(self) -> None:
        self._flag_numbering = menu_tools.create_number_name_map(self._subject.all_flag_names)

    def configure(self, subject: 'SupportsFlagSetting', return_to: str,
                  backup_flag_data: Dict[str, Optional[bool]]) -> None:
        self._subject = subject
        self._return_to_route = return_to
        self._backup_flag_data = backup_flag_data

    @property
    def _flag_menu(self) -> str:
        output = ''
        for flag_number in self._flag_numbering:
            output = output + '{num}. {name}: {value}\n'.format(
                num=flag_number,
                name=self._flag_numbering[flag_number],
                value=self._subject.summarise_flag(self._flag_numbering[flag_number])
            )
        return output

    def _print_main_menu(self) -> str:
        output = _main_menu_template.format(flag_menu=styles.fore(self._flag_menu, 'blue'))
        return self.app.fetch_component('standard_page_component').print(
            page_title='Flag Editor',
            page_content=output
        )

    def _validate_flag_num(self, value: Any) -> int:
        try:
            value = int(value)
        except ValueError:
            raise ResponseValidationError('The flag number was not recognised.')
        if value not in self._flag_numbering.keys():
            raise ResponseValidationError('{} does not refer to a flag.'.format(value))
        return value

    def _on_ok(self) -> None:
        self.app.goto(self._return_to_route)

    def _on_cancel(self) -> None:
        self._subject.set_flags(self._backup_flag_data)  # TODO - Implement this;

    def _on_yes(self, args):
        self._subject.set_flag(self._flag_numbering[args['flag_num']], True)

    def _on_no(self, args) -> None:
        self._subject.set_flag(self._flag_numbering[args['flag_num']], False)

    def _on_unset(self, args) -> None:
        self._subject.set_flag(self._flag_numbering[args['flag_num']], None)
