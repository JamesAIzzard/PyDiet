from pydiet.tags import i_taggable

def print_enumerated_active_tags(subject:'i_taggable.ITaggable')->str:
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