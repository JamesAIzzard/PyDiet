from typing import List, Dict
from difflib import SequenceMatcher

def score_similarity(words: List[str], search_term: str) -> Dict[str, float]:
    scores = {}
    for word in words:
        scores[word] = SequenceMatcher(None, search_term, word).ratio()
    return scores