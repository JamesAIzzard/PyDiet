from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from pydiet.flags.supports_flags import SupportsFlags

def print_numbered_flags_menu(flags:List[str]) -> str:
    output = ''
    if len(flags):
        for i, flag_name in enumerate(flags, start=1):
            output = output + '{num}. {flag_name}\n'.format(
                num=i,
                flag_name=flag_name)
    else:
        output = 'No flags assigned.'
    return output


def print_numbered_true_flags_menu(subject: 'SupportsFlags') -> str:
    return print_numbered_flags_menu(subject.true_flags)


def print_numbered_false_flags_menu(subject: 'SupportsFlags') -> str:
    return print_numbered_flags_menu(subject.false_flags)


def print_numbered_undefined_flags_menu(subject: 'SupportsFlags') -> str:
    return print_numbered_flags_menu(subject.undefined_flags)


def print_flag_summary(flag_name: str, flag_value: Optional[bool]) -> str:
    return '{flag_name}: {flag_value}'.format(
        flag_name=flag_name,
        flag_value=flag_value
    )
