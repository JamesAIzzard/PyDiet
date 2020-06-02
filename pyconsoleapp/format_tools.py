def sentence_case(text: str) -> str:
    '''Capitalizes the first letter of each word in the
    text provided.

    Args:
        text (str): Text to convert to sentence case.

    Returns:
        str: Text with sentence case capitalisation.
    '''
    words_list = text.split('_')
    for word in words_list:
        word.capitalize()
    return ' '.join(words_list)
