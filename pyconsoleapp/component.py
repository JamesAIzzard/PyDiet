import abc
from typing import List, Callable, Optional, Type, TypeVar, TYPE_CHECKING

from pyconsoleapp import exceptions, statemap, responder

if TYPE_CHECKING:
    from pyconsoleapp.statemap import Statemap
    from pyconsoleapp import ConsoleApp
    from pyconsoleapp.responder_args import ResponderArg
    from pyconsoleapp.responder import Responder

T = TypeVar('T')


class Component(abc.ABC):
    """Base class for all application components."""

    def __init__(self, app: 'ConsoleApp', state_map: Optional['Statemap'] = None, **kwds):
        self._app = app
        if state_map is None:
            state_map = statemap.Statemap({"main": self})
        self._statemap: 'Statemap' = state_map
        self._child_components: List['Component'] = []
        self._local_responders: List['Responder'] = []  # 'local' indicates on *this* instance, not children.
        self._get_view_prefill: Optional[Callable[..., str]] = None
        self.loaded_once: bool = False

    @property
    def app(self) -> 'ConsoleApp':
        """Returns the component's app reference."""
        return self._app

    @abc.abstractmethod
    def printer(self, **kwds) -> str:
        """Abstract method responsible for rendering the component view into text."""
        raise NotImplementedError

    @property
    def single_hr(self) -> str:
        """Returns a unicode single horizontal rule, as long as the terminal width set in configs."""
        return u'\u2500' * self.app.terminal_width

    @property
    def double_hr(self) -> str:
        """Returns a unicode double horizonal rule, as long as the terminal width set in configs."""
        return u'\u2501' * self.app.terminal_width

    def on_load(self) -> None:
        """Method run immediately before the view is extracted from the component."""

    def on_first_load(self) -> None:
        """Method run the first time the component is used."""

    def _validate(self) -> None:
        """Checks the component is valid. Raises an exception if not."""
        # Check there are not multiple local ArglessResponders or markerless args;
        argless_found = False
        markerless_found = False
        for local_responder in self._local_responders:
            if local_responder.is_argless:
                if argless_found is False:
                    argless_found = True
                elif argless_found is True:
                    raise exceptions.DuplicateArglessResponderError
            if local_responder.has_markerless_arg:
                if markerless_found is False:
                    markerless_found = True
                elif markerless_found is True:
                    raise exceptions.DuplicateMarkerlessArgError

    @property
    def states(self) -> List[str]:
        """Returns a list of all states associated with this component and its siblings."""
        return list(self._statemap.keys())

    @property
    def current_state(self) -> str:
        """Returns the siblings' current state."""
        return self._statemap.current_state

    @current_state.setter
    def current_state(self, state: str) -> None:
        """Sets the siblings' current state."""
        self._statemap.current_state = state

    def get_state_changer(self, new_state: str) -> Callable[[], None]:
        """Returns a function, which, when called, changes the siblings' state to the state specified."""

        def changer():
            self._statemap.current_state = new_state

        return changer

    @property
    def active_components(self) -> List['Component']:
        """Returns the components associated with the siblings' current state."""
        components = [self]
        for child_component in self._child_components:
            child_active_sibling = child_component.get_sibling()
            for active_component in child_active_sibling.active_components:
                if active_component not in components:
                    components.append(active_component)
        return components

    def get_sibling(self, state: Optional[str] = None) -> 'Component':
        """Returns the sibling (maybe self) associated with the specified state. If no state is specified,
        returns the sibling for the current state."""
        if state is None:
            state = self._statemap.current_state
        try:
            return self._statemap[state]
        except KeyError:
            raise exceptions.StateNotFoundError

    @property
    def local_responders(self) -> List['Responder']:
        """Returns a list of responders local to this component."""
        return self._local_responders

    def configure_responder(self, responder_func: Callable[..., None], args: Optional[List['ResponderArg']] = None):
        """Returns the correct responder type, with it's app reference configured."""
        return responder.Responder(app=self.app, func=responder_func, args=args)

    @property
    def active_responders(self) -> List['Responder']:
        """Returns a list of active responders for this component and its children."""
        active_responders = []
        for active_component in self.active_components:
            active_responders.extend(active_component.local_responders)
        return active_responders

    @property
    def active_argless_responder(self) -> Optional['Responder']:
        """Returns the argless responder for this state combo, if exists, otherwise returns None."""
        argless_responder = None
        for active_responder in self.active_responders:
            if active_responder.is_argless:
                if argless_responder is None:
                    argless_responder = active_responder
                elif argless_responder is not None:
                    raise exceptions.DuplicateArglessResponderError
        return argless_responder

    @property
    def active_markerless_arg_responder(self) -> Optional['Responder']:
        """Returns the component's markerless arg responder, if exists, otherwise returns None."""
        markerless_arg_responder = None
        for active_responder in self.active_responders:
            if active_responder.has_markerless_arg:
                if markerless_arg_responder is None:
                    markerless_arg_responder = active_responder
                elif markerless_arg_responder is not None:
                    raise exceptions.DuplicateMarkerlessArgError
        return markerless_arg_responder

    @property
    def active_marker_arg_responders(self) -> List['Responder']:
        """Returns a list of the component's marker responders."""
        mars = []
        for active_responder in self.active_responders:
            if not active_responder.has_markerless_arg and not active_responder.is_argless:
                mars.append(active_responder)
        return mars

    def get_view_prefill(self) -> Optional[str]:
        """Returns the prefill for the component."""
        if self._get_view_prefill is not None:
            return self._get_view_prefill()
        else:
            return None

    def delegate_state(self, state: str, component_class: Type[T]) -> T:
        """Instantiates the sibling component to run the specified state, adds it to the statemap
        and returns it."""
        component = component_class(app=self.app, state_map=self._statemap)
        self._statemap[state] = component
        return component

    def use_component(self, component_class: Type[T]) -> T:
        """Includes the child component in this component instance and returns the child instance."""
        component = component_class(app=self.app)
        self._child_components.append(component)
        list(set(self._child_components))  # Use set() to prevent duplication.
        return component

    def configure(self, responders: Optional[List['Responder']] = None,
                  get_prefill: Optional[Callable[[], str]] = None,
                  **kwds) -> None:
        """Implements post-initialistion configuration of the component."""
        if responders is not None:
            for r in responders:
                if r not in self._local_responders:
                    self._local_responders.append(r)

        if get_prefill is not None:
            self._get_view_prefill = get_prefill

        self._validate()
        # Swallow any remaining **kwds and check this really is the base class.
        assert not hasattr(super(), 'configure')
