"""Implements functionality associated with assigning instructions to an instance.
Examples:
    Recipe instances can have instructions assigned.
"""
import abc
from typing import Dict, Optional, Any

import persistence


class HasReadableInstructionSrc(persistence.YieldsPersistableData, abc.ABC):
    """Implements functionality associated with assigning a readable instruction source."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    @abc.abstractmethod
    def instruction_src(self) -> str:
        """Returns instruction source for the instance."""
        raise NotImplementedError

    @property
    def instruction_src_defined(self) -> bool:
        """Returns True/False to indicate if the instruction source is defined."""
        return self.instruction_src is not None

    @property
    def persistable_data(self) -> Dict[str, Any]:
        """Returns the persistable data for the instance."""
        data = super().persistable_data
        data['instruction_src'] = self.instruction_src
        return data


class HasSettableInstructionSrc(HasReadableInstructionSrc, persistence.CanLoadData):
    """Implements functionality assoicated with supporting a settable instruction source."""

    def __init__(self, instruction_src_data: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)

        # Create local stash for instruction source;
        self._instruction_src: Optional[str] = None

        if instruction_src_data is not None:
            self.load_data({'instruction_src': instruction_src_data})

    @property
    def instruction_src(self) -> str:
        """Returns the instruction src for the instance."""
        return self._instruction_src

    @instruction_src.setter
    def instruction_src(self, instruction_src: str) -> None:
        """Sets the instruction src for the instance."""
        self._instruction_src = instruction_src

    def load_data(self, data: Dict[str, Any]) -> None:
        """Loads data into the test instance."""
        super().load_data(data)

        if 'instruction_src' in data.keys():
            self._instruction_src = data['instruction_src']
