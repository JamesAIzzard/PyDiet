"""Implements functionality associated with saving historical solutions."""
import os
import json
from typing import List, Tuple

import model


class History:
    """Implements functionality to record the evolution history."""

    def __init__(self):
        self._historical_solutions: List[Tuple[int, 'model.meals.MealData']] = []

    def record_solution(self, gen: int, solution_data: 'model.meals.MealData'):
        """Records the solution provided."""
        self._historical_solutions.append((gen, solution_data))
        with open("history.json", 'w') as fh:
            json.dump(self._historical_solutions, fh)
