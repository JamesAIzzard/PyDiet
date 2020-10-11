import abc
import copy
from typing import Dict


class SupportsSteps:
    @property
    @abc.abstractmethod
    def _step_data(self) -> Dict[int, str]:
        return self._step_data

    @property
    def step_data(self) -> Dict[int, str]:
        return copy.deepcopy(self._step_data)

    @property
    def step_summary(self) -> str:
        return 'Step summary.'


class SupportsSettingSteps(SupportsSteps):
    @property
    def step_data(self) -> Dict[int, str]:
        return self._step_data
