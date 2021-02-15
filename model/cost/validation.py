from model import cost


def validate_cost(cost_per_g: float) -> float:
    if cost_per_g >= 0:
        return float(cost_per_g)
    else:
        raise cost.exceptions.CostValueError
