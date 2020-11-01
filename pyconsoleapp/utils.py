from difflib import SequenceMatcher
from heapq import nlargest
from textwrap import fill
from typing import Dict, List, Optional, TypeVar

from pyconsoleapp import configs

T = TypeVar('T')


def wrap_text(text: str, num_chars: Optional[int] = None) -> str:
    """Wraps the text to the specified width (number of chars). If no width is specified, the text is
    wrapped to the console width defined in the configs."""
    if num_chars is None:
        num_chars = configs.terminal_width_chars
    return fill(text, num_chars)


def truncate_text(text: str, num_chars: int, end_chars: str = '...') -> str:
    """Truncates the text to the specified number of characters (minus length of end chars) and adds the end chars."""
    if len(text) < num_chars - len(end_chars):
        end_chars = ''
    return text[:num_chars - len(end_chars)] + end_chars


def sentence_case(text: str) -> str:
    """Returns the text with the first letter of each word capitalised."""
    words_list = text.split('_')
    for word in words_list:
        word.capitalize()
    return ' '.join(words_list)


def make_numbered_map(list_to_map: List[T], start_num: int = 1) -> Dict[int, T]:
    """Converts a list of T into a dictionary of T with integer keys, starting at start_num. If start_num
    is not specified, it defaults to 1."""
    return dict(enumerate(list_to_map, start=start_num))


def score_similarity(words_to_score: List[str], search_term: str) -> Dict[str, float]:
    """Returns a dictionary of the each word in the original list, coupled with a similarity score indicating
    how similar each word is to the similarity term."""
    scores = {}
    for word in words_to_score:
        scores[word] = SequenceMatcher(None, search_term, word).ratio()
    return scores


def get_n_best_matches(words_to_search: List[str], search_term: str, num_results: int) -> List[str]:
    """Returns a list of n words most similar to the search term."""
    all_scores = score_similarity(words_to_search, search_term)
    return nlargest(num_results, all_scores, key=all_scores.get)
