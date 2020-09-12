from pydiet import cost

def validate_cost(cost_value:float) -> float:
    try:
        cost_value = float(cost_value)
    except ValueError:
        raise cost.exceptions.InvalidCostValueError
    if cost_value < 0:
        raise cost.exceptions.InvalidCostValueError
    return cost_value
