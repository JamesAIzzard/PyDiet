from typing import Union, Optional, Any

import model


class BaseCostError(model.exceptions.PyDietModelError):
    """Base class for cost module exceptions."""

    def __init__(self,
                 subject: Optional[Union[
                     'model.cost.HasReadableCostPerQuantity',
                     'model.cost.HasSettableCostPerQuantity']
                 ] = None, **kwargs):
        super().__init__(**kwargs)
        self.subject = subject


class CostNotSettableError(BaseCostError, TypeError):
    """Indicates the subject does not support cost setting."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class UndefinedCostError(BaseCostError):
    """Indicating the cost is not defined."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class InvalidCostError(BaseCostError, ValueError):
    """Indicating the qty provided is not a valid cost."""

    def __init__(self, invalid_value: Any, **kwargs):
        super().__init__(**kwargs)
        self.invalid_value = invalid_value
