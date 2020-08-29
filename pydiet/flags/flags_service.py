from typing import Optional, List

from pydiet import flags


def print_numbered_flags_menu(flags: List[flags.flag.Flag]) -> str:
    output = ''
    if len(flags):
        for i, flag in enumerate(flags, start=1):
            output = output + '{num}. {flag_name}\n'.format(
                num=i,
                flag_name=flag.name)
    else:
        output = 'No flags assigned.'
    return output


def print_numbered_true_flags_menu(subject: flags.supports_flags.SupportsFlags) -> str:
    return print_numbered_flags_menu(subject.true_flags)


def print_numbered_false_flags_menu(subject: flags.supports_flags.SupportsFlags) -> str:
    return print_numbered_flags_menu(subject.false_flags)


def print_numbered_undefined_flags_menu(subject: flags.supports_flags.SupportsFlags) -> str:
    return print_numbered_flags_menu(subject.undefined_flags)


def print_flag_summary(flag_name: str, flag_value: Optional[bool]) -> str:
    return '{flag_name}: {flag_value}'.format(
        flag_name=flag_name,
        flag_value=flag_value
    )
