"""Implements functionality associated with saving historical solutions."""
import json
from typing import List, Tuple

import model
from optimisation import configs


class History:
    """Implements functionality to record the evolution history."""

    def __init__(self, history_filepath: str = configs.history_path):
        self.history_filepath: str = history_filepath
        self._historical_solution_data: List[Tuple[int, 'model.meals.MealData']] = []

    def record_solution(self, gen: int, solution_data: 'model.meals.MealData'):
        """Records the solution provided."""
        self._historical_solution_data.append((gen, solution_data))
        with open(self.history_filepath, 'w') as fh:
            json.dump(self._historical_solution_data, fh, indent=2)
