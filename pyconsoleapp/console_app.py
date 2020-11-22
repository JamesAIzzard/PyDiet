import os
from typing import Dict, List, Optional, TYPE_CHECKING, Type, TypeVar

from pyconsoleapp import exceptions, configs, component

if os.name == 'nt':
    from pyautogui import write  # noqa
else:
    import readline  # noqa

if TYPE_CHECKING:
    from pyconsoleapp import Component, GuardComponent

T = TypeVar('T')


def _write_to_screen(view: str, prefill: Optional[str]):
    """Adds the option of prefill to the normal input() function."""
    if prefill is None:
        prefill = ''
    if os.name == 'nt':
        write(prefill)
        return input(view)
    else:
        readline.set_startup_hook(lambda: readline.insert_text(prefill))
        try:
            return input(view)
        finally:
            readline.set_startup_hook()


class ConsoleApp:
    def __init__(self, name):
        self._name: str = name
        self._response: Optional[str] = None
        self._current_route: Optional[str] = None
        self._route_history: List[str] = []
        self._route_component_map: Dict[str, 'Component'] = {}
        self._initialising: bool = False
        self._route_exit_guard_map: Dict[str, 'GuardComponent'] = {}
        self._route_entrance_guard_map: Dict[str, 'GuardComponent'] = {}
        self._finished_processing_response: bool = False
        self._quit: bool = False
        self.error_message: Optional[str] = None
        self.info_message: Optional[str] = None

    @property
    def name(self) -> str:
        """Gets application name."""
        return self._name

    @property
    def current_route(self) -> str:
        """Gets the current application route."""
        if self._current_route is None:
            raise exceptions.NoCurrentRouteError
        return self._current_route

    @current_route.setter
    def current_route(self, route: str) -> None:
        """Sets the current application route."""
        if route in self._route_component_map.keys():
            self._current_route = route
        else:
            raise KeyError('The route {} was not recognised.'.format(route))

    def _validate_route(self, route: str):
        """Raises an exception if the route is not in the set of known routes."""
        if route not in self._route_component_map:
            raise exceptions.InvalidRouteError

    def _historise_route(self, route: str) -> None:
        """Adds the route to the route history stack, if it is not already the same as the last item."""
        # Save the current route to the history;
        self._validate_route(route)
        if len(self._route_history) > 0 and not self._route_history[-1] == route:
            self._route_history.append(route)
        # Make sure the history doesn't get too long;
        while len(self._route_history) > configs.route_history_length:
            self._route_history.pop(0)

    def get_component(self, component_class: Type[T], route: str, state: Optional[str] = None) -> T:
        """Gets the component associated with the specified route and state. If state is not
        specified, the component corresponding to the route's current state is returned.

        Raises:
            PartiallyInitialisedError: To indicate the application is still initialising components,
                so we can't start retrieving them yet.
        """
        if self._initialising is True:
            raise exceptions.PartiallyInitialisedError
        self._validate_route(route)  # Check the route is recognised;
        # Grab the component registered the route;
        comp = self._route_component_map[route].get_sibling(state)
        assert isinstance(comp, component_class)
        return comp

    def _get_active_component(self) -> 'Component':
        """Returns the component/guard corresponding with current application state."""
        # Check for active guard;
        active_guard = self._get_active_guard()
        if active_guard is not None:
            return active_guard
        return self.get_component(component.Component, self.current_route)

    def _get_active_guard(self) -> Optional['GuardComponent']:
        """Returns the active guard if exists, otherwise returns None."""
        guard: Optional['GuardComponent'] = None
        # First check the exit guards;
        for guarded_route in self._route_exit_guard_map.keys():
            # If the guarded root does not feature in the submitted route;
            if guarded_route not in self.current_route:
                # The submitted route must have exited, so populate the component;
                guard = self._route_exit_guard_map[guarded_route]
                break
        # Now check the entrance guards;
        for guarded_route in self._route_entrance_guard_map.keys():
            # If the guarded root is part of the submitted route;
            if guarded_route in self.current_route:
                # Then the submitted route must be beyond the guard, so populate the
                # component;
                guard = self._route_entrance_guard_map[guarded_route]
        # Return the guard if it is populated & activated.
        if guard is not None and guard.activated:
            return guard
        else:
            return None

    def guard_entrance(self, route_to_stay_outside: str, guard_class: Type[T]) -> T:
        """Instantiates the guard, assigns it to guard entrance of the specified route, and returns it."""
        self._validate_route(route_to_stay_outside)
        guard = guard_class(app=self)  # type: GuardComponent
        self._route_entrance_guard_map[route_to_stay_outside] = guard
        return guard

    def guard_exit(self, route_to_stay_within: str, guard_class: Type[T]) -> T:
        """Instantiates the guard, assigns it to guard exit of the specified route, and returns it."""
        self._validate_route(route_to_stay_within)
        guard = guard_class(app=self)  # type: GuardComponent
        self._route_exit_guard_map[route_to_stay_within] = guard
        return guard

    def clear_entrance(self, route: str) -> None:
        """Clears any guard from the entrance of the specified route."""
        self._validate_route(route)
        if route in self._route_entrance_guard_map.keys():
            del self._route_entrance_guard_map[route]

    def clear_exit(self, route: str) -> None:
        """Clears any guard from the exit of the specified route."""
        self._validate_route(route)
        if route in self._route_exit_guard_map.keys():
            del self._route_exit_guard_map[route]

    def clear_guard(self, guard_instance: 'GuardComponent') -> None:
        """Removes the guard from the entrance/exit route-guard maps."""
        self._route_exit_guard_map = {k: v for k, v in self._route_exit_guard_map.items() if not v == guard_instance}
        self._route_entrance_guard_map = {k: v for k, v in self._route_entrance_guard_map.items() if
                                          not v == guard_instance}

    def _process_response(self, response: str) -> None:
        """Processes the response provided.
        - If the response is empty, the active cli are searched for an empty responder, which, if found, is
        called with no arguments.
        - If the response is not empty the active cli are searched for a matching marker-responder, which
        if found, is called with the response as an argument.
        - If no marker responders are found, the active cli are searched for a markerless responder, which if
        found, is called with the response as an argument."""
        responder_was_found = False
        current_component = self._get_active_component()
        try:
            # If the response is empty, give each active component a chance to respond;
            if response.replace(' ', '') == '':
                argless_responder = current_component.active_argless_responder
                if argless_responder:
                    argless_responder.respond()
                    responder_was_found = True
                    if self._finished_processing_response:
                        return

            # Otherwise, give any marker-only responders a chance;
            else:
                responders = current_component.active_marker_arg_responders
                if len(responders):
                    for responder in responders:
                        if responder.check_marker_match(response):
                            responder.respond(response)
                            responder_was_found = True
                            if self._finished_processing_response:
                                return

            # Finally give each active component a chance to field a
            # markerless responder;
            markerless_responder = current_component.active_markerless_arg_responder
            if markerless_responder:
                markerless_responder.respond(response)
                responder_was_found = True
                if self._finished_processing_response:
                    return

            # If no component has responded, then raise an exception;
            if not responder_was_found and not response.replace(' ', '') == '':
                raise exceptions.ResponseValidationError('This response isn\'t recognised.')

        except exceptions.ResponseValidationError as e:
            if e.reason is not None:
                self.error_message = e.reason
            return

    def _clear_response(self):
        """Resets the response fields, ready for the next response collection cycle."""
        self._response = None
        self._finished_processing_response = False

    def continue_responding(self) -> None:
        """Instructs the application to continue searching for responders."""
        self._finished_processing_response = False

    def stop_responding(self) -> None:
        """Instructs the application to stop searching for responders."""
        self._finished_processing_response = True

    def run(self) -> None:
        """Main run loop for the CLI."""
        while not self._quit:
            # If response has been collected;
            if self._response is not None:
                # Reset the error and info messages;
                self.error_message = None
                self.info_message = None
                # Do the processing;
                self._process_response(self._response)
                self._clear_response()

            # The response has not been collected, draw the view and collect it;
            else:
                active_component = self._get_active_component()
                if not active_component.loaded_once:
                    active_component.on_first_load()
                    active_component.loaded_once = True
                active_component.on_load()
                # Check the component is still the right one after the load method ran.
                if not active_component == self._get_active_component():
                    continue
                #
                self._historise_route(self.current_route)
                # Draw the view;
                self.clear_console()
                self._response = _write_to_screen(view=active_component.printer(),
                                                  prefill=active_component.get_view_prefill())

    def go_to(self, route: str) -> None:
        """Navigates the application the specified route."""
        self._validate_route(route)
        # Set the new route;
        self.current_route = route

    def go_back(self) -> None:
        """Returns the current route to the previous route in the route history."""
        self.current_route = self._route_history.pop()

    def configure(self, routes: Optional[Dict[str, Type['Component']]] = None,
                  **kwds) -> None:  # noqa: Ignore unused kwds warning.
        """Configures the application routes and swallows any remaining keywords."""
        if routes is not None:
            self._initialising = True
            for route, component_class in routes.items():
                self._route_component_map[route] = component_class(app=self)
            self._initialising = False
        # Check we don't have a superclass that also wants configuration;
        assert not hasattr(super(), 'configure')

    @staticmethod
    def clear_console():
        os.system('cls' if os.name == 'nt' else 'clear')

    @property
    def terminal_width(self) -> int:
        return configs.terminal_width_chars

    def quit(self):
        self._quit = True
