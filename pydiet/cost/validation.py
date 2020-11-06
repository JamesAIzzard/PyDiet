from pydiet.cost import exceptions


def validate_cost(cost_per_g: float) -> float:
    if cost_per_g >= 0:
        return float(cost_per_g)
    else:
        raise exceptions.CostValueError
