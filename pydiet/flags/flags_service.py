from typing import Optional

from pydiet import flags

def print_active_flags_menu(subject:'flags.i_has_flags.IHasFlags'):
    output = ''
    if len(subject.flags):
        for i,flag_name in enumerate(subject.flags, start=1):
            output = output + '{num}. {flag_name}\n'.format(
                num=i,
                flag_name=flag_name)
    else:
        output = 'No flags assigned.'
    return output

def print_flag_summary(flag_name:str, flag_value:Optional[bool])->str:
    return '{flag_name}: {flag_value}'.format(
        flag_name=flag_name,
        flag_value=flag_value
    )