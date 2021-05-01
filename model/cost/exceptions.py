from typing import Union, Optional

import model


class BaseCostError(model.exceptions.PyDietModelError):
    """Base class for cost module exceptions."""

    def __init__(self,
                 subject: Optional[Union[
                     'model.cost.SupportsCost',
                     'model.cost.SupportsSettableCost']
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


class CostValueError(BaseCostError, ValueError):
    """Indicating the qty provided is not a valid cost."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
