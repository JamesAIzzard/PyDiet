"""Validation functions for the cost module."""
from model import cost


def validate_cost(cost_value: float) -> float:
    """Validates a potential cost value."""
    try:
        if cost_value >= 0:
            return float(cost_value)
        else:
            raise cost.exceptions.InvalidCostError(invalid_value=cost_value)
    except TypeError:
        raise cost.exceptions.InvalidCostError(invalid_value=cost_value)