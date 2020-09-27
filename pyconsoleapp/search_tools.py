from difflib import SequenceMatcher
from heapq import nlargest
from typing import List, Dict


def score_similarity(words_to_score: List[str], search_term: str) -> Dict[str, float]:
    scores = {}
    for word in words_to_score:
        scores[word] = SequenceMatcher(None, search_term, word).ratio()
    return scores


def search_n_best_matches(words_to_search: List[str], search_term: str, num_results: int) -> List[str]:
    all_scores = score_similarity(words_to_search, search_term)
    return nlargest(num_results, all_scores, key=all_scores.get)
