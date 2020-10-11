import abc
import copy
from typing import List


class SupportsServeTimes(abc.ABC):
    @property
    @abc.abstractmethod
    def _serve_times_data(self) -> List[str]:
        raise NotImplementedError

    @property
    def serve_times_data(self) -> List[str]:
        return copy.deepcopy(self._serve_times_data)

    @property
    def serve_times_summary(self) -> str:
        return 'Serve times summary'


class SupportsSettingServeTimes(SupportsServeTimes, abc.ABC):
    @property
    def serve_times_data(self) -> List[str]:
        return self._serve_times_data
