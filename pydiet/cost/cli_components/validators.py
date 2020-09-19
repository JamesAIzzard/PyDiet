from pyconsoleapp import ResponseValidationError

from pydiet import cost


def validate_cost(cost_value: float) -> float:
    try:
        cost_value = cost.cost_service.validate_cost(cost_value)
    except cost.exceptions.CostValueError:
        raise ResponseValidationError('The cost must be a positive number')
    return cost_value
