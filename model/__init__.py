"""Initialisation for the model module."""
from .main import (
    HasName,
    HasSettableName,
    SupportsDefinition,
    HasMandatoryAttributes
)

from . import exceptions
from . import configs
from . import quantity
from . import cost
from . import nutrients
from . import flags
from . import time
from . import tags
from . import ingredients
