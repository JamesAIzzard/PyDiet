from typing import List, Dict, TYPE_CHECKING

from pydiet.optimisation import optimisation_service as ops

if TYPE_CHECKING:
    from pydiet.optimisation.day_goals import DayGoals
    from pydiet.optimisation.day_solution import DaySolution


def solve_day_goals(day_goals: List['DayGoals'], num_solutions: int, ignore_recipes: List[str]) -> Dict[str, List['DaySolution']]:
    # Place to put solutions;
    solutions = {}
    # Cycle through the day goals and solve;
    for dg in day_goals:
        solutions[dg.name] = solve_day_goal(dg, num_solutions, ignore_recipes)
    # Return
    return solutions


def solve_day_goal(day_goal: 'DayGoals', num_solutions: int, ignore_recipes: List[str]) -> List['DaySolution']:
    raise NotImplementedError
