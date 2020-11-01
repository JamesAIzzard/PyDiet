from collections.abc import MutableMapping
from typing import Dict, Iterator, TYPE_CHECKING

from pyconsoleapp import exceptions

if TYPE_CHECKING:
    from pyconsoleapp import Component


class Statemap(MutableMapping):
    def __init__(self, state_map: Dict[str, 'Component']):
        self._current_state: str = "main"
        self._state_component_map = state_map

    @property
    def current_state(self) -> str:
        """Returns the currently selected state."""
        return self._current_state

    @current_state.setter
    def current_state(self, state: str) -> None:
        """Sets the current state."""
        self.validate_state(state)
        self._current_state = state

    def validate_state(self, state: str) -> None:
        """Raises an exception if the current state is not in the list of known states."""
        if state not in self.keys():
            raise exceptions.StateNotFoundError

    def __getitem__(self, key: str) -> 'Component':
        return self._state_component_map[key]

    def __setitem__(self, key: str, value: 'Component') -> None:
        self._state_component_map[key] = value

    def __delitem__(self, key: str) -> None:
        del self._state_component_map[key]

    def __iter__(self) -> Iterator:
        return iter(self._state_component_map)

    def __len__(self) -> int:
        return len(self._state_component_map)
