from typing import Dict

from pyconsoleapp import ConsoleAppComponent, menu_tools

_main_menu_template = '''
----------------|-------------------
Save Changes    | -save
----------------|-------------------
Mark Flag Yes   | -yes [flag number]
Mark Flag No    | -no  [flag number]
Unset Flag      | -del [flag number]
----------------|-------------------

Set Flags:
{current_flags}

Unset Flags:
{available_flags}
'''


class FlagEditorComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self.subject
        self.current_flag_num_map: Dict[int, str]
        self.available_flag_num_map: Dict[int, str]
        self.set_response_function(['-add', '-a'], self.on_add_flag)
        self.set_response_function(['-remove', '-r'], self.on_remove_flag)

    def run(self) -> None:
        self.current_flag_num_map = menu_tools.create_number_name_map(
            self.subject.flags)
        self.available_flag_num_map = menu_tools.create_number_name_map(
            self.subject.available_flags)

    def print(self, *args, **kwargs) -> str:
        output = _MAIN_TEMPLATE.format(
            current_flags=self.current_flags_menu,
            available_flags=self.available_flags_menu
        )
        return self.app.fetch_component('standard_page_component').call_print(output)

    @property
    def current_flags_menu(self) -> str:
        if len(self.current_flag_num_map) == 0:
            return 'No flags added.'
        output = ''
        for flag_num in self.current_flag_num_map.keys():
            output = output + '{flag_num} -> {flag_name}\n'.format(
                flag_num=flag_num,
                flag_name=self.current_flag_num_map[flag_num]
            )
        return output

    @property
    def available_flags_menu(self) -> str:
        if len(self.available_flag_num_map) == 0:
            return 'No flags available.'
        output = ''
        for flag_num in self.available_flag_num_map.keys():
            output = output + '{flag_num} -> {flag_name}\n'.format(
                flag_num=flag_num,
                flag_name=self.available_flag_num_map[flag_num]
            )
        return output

    def on_add_flag(self, args=None) -> None:
        # Check the args is a number referring to an available flag;
        try:
            args = int(args)
        except ValueError:
            self.app.error_message = 'Specify a number from the available flags menu.'
            return
        if not args in self.available_flag_num_map.keys():
            self.app.error_message = 'Specify a number from the available flags menu.'
            return
        # Add the flag;
        self.subject.add_flag(self.available_flag_num_map[args])

    def on_remove_flag(self, args=None) -> None:
        # Check the args is a number referring to a current flag;
        try:
            args = int(args)
        except ValueError:
            self.app.error_message = 'Specify a number from the current flags menu.'
            return
        if not args in self.current_flag_num_map.keys():
            self.app.error_message = 'Specify a number from the current flags menu.'
            return
        # Remove the flag;
        self.subject.remove_flag(self.current_flag_num_map[args])
