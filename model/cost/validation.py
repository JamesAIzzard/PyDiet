from model import cost


def validate_cost(cost_value: float) -> float:
    if cost_value >= 0:
        return float(cost_value)
    else:
        raise cost.exceptions.CostValueError
