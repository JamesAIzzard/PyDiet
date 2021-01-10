from pydiet import tags

def print_enumerated_active_tags(subject:'tags.i_has_tags.IHasTags')->str:
    output = ''
    if len(subject.tags):
        for i,tag in enumerate(subject.tags, start=1):
            output = output + '{num}. {tag}'.format(
                num=i,
                tag=tag
            )
    else:
        output = 'No tags assigned.'
    return output