import abc
import copy
from typing import List


class SupportsTags:

    @property
    @abc.abstractmethod
    def _tag_data(self) -> List[str]:
        raise NotImplementedError

    @property
    def tag_data(self) -> List[str]:
        return copy.deepcopy(self._tag_data)

    @property
    def tag_summary(self) -> str:
        return 'Tag summary.'


class SupportsSettingTags(SupportsTags):
    @property
    @abc.abstractmethod
    def tag_data(self) -> List[str]:
        return self._tag_data

