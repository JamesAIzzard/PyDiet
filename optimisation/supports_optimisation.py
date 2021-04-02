import abc
from typing import Dict, Any


class SupportsOptimisation:

    @property
    @abc.abstractmethod
    def genes(self) -> Dict[str, Any]:
        """Returns a Dict of genes specifying the DOF in individual."""
