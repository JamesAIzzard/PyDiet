from pydiet import cost

def validate_cost(cost_value:float) -> float:
    try:
        cost_value = float(cost_value)
    except ValueError:
        raise cost.exceptions.CostValueError
    if cost_value < 0:
        raise cost.exceptions.CostValueError
    return cost_value
