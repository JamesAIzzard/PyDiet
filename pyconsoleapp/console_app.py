import os, re, importlib
from pyconsoleapp.exceptions import ResponseValidationError
from importlib import util
from typing import Callable, Dict, List, Optional, TYPE_CHECKING, cast
if os.name == 'nt':
    from pyautogui import write
else:
    import readline

import pyconsoleapp as pcap

if TYPE_CHECKING:
    from pyconsoleapp.components import (
        ConsoleAppComponent,
        ConsoleAppGuardComponent
    )


def pascal_to_snake(text: str) -> str:
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def snake_to_pascal(text: str) -> str:
    return ''.join(x.capitalize() or '_' for x in text.split('_'))


def rlinput(prompt, prefill=''):
    if os.name == 'nt':
        write(prefill)
        return input(prompt)
    else:
        readline.set_startup_hook(lambda: readline.insert_text(prefill))
        try:
            return input(prompt)
        finally:
            readline.set_startup_hook()


class ConsoleApp():
    def __init__(self, name):
        self._response: Optional[str] = None
        self._root_route: str = ''
        self._route: str = ''
        self._route_history: List[str] = []
        self._route_component_maps: Dict[str, str] = {}
        self._route_exit_guard_map: Dict[str, 'ConsoleAppGuardComponent'] = {}
        self._route_entrance_guard_map: Dict[str, 'ConsoleAppGuardComponent'] = {}
        self._components: Dict[str, 'ConsoleAppComponent'] = {}
        self._active_components: List['ConsoleAppComponent'] = []
        self._component_packages: List[str] = []
        self._finished_responding: bool = False        
        self._quit: bool = False
        self.name: str = name
        self.error_message: Optional[str] = None
        self.info_message: Optional[str] = None

    @property
    def _active_response_functions(self) -> Dict[str, Callable]:
        '''Returns a dict of all currently active option responses.

        Returns:
            Dict[str, Callable]: A dict of all currently active option
            responses.
        '''
        # Collect the response function map from each active component;
        response_functions = {}
        for component in self._active_components:
            response_functions.update(component._response_functions)
        # Then return them;
        return response_functions

    @property
    def route(self) -> str:
        if self._route == '':
            return self._root_route
        else:
            return self._route

    @route.setter
    def route(self, route: str) -> None:
        route = self.interpret_relative_route(route)
        # If the route was recognised, set it;
        if route in self._route_component_maps.keys():
            self._route = route
        # Otherwise, shout;
        else:
            raise KeyError('The route {} was not recognised.'.format(route))

    def root_route(self, route: str, component_class_name: str) -> None:
        self._root_route = route
        self.add_route(route, component_class_name)

    def add_route(self, route: str, component_class_name: str) -> None:
        self._route_component_maps[route] = \
            pascal_to_snake(component_class_name)

    def interpret_relative_route(self, route: str) -> str:
        '''Converts a relative route with point notation
        preceeding it, to an absolute route from the
        root route.

        Arguments:
            route {str} -- Route, possibly containing relative
                point notation.

        Returns:
            str -- Absolute route.
        '''
        # Figure out how many reverses were in the route;
        back_counter = -1
        while len(route) and route[0] == '.':
            # Increment the reverse counter;
            back_counter = back_counter + 1
            # Knock the front dot off;
            route = route[1:]
        # If it wasn't a relative route at all, just return;
        if back_counter == -1:
            # Just return the route unchanged;
            return route
        # If it was a relative route with no reverses;
        elif back_counter == 0:
            # Also if we are appending, put a dot in front of the new part;
            if route:
                route = '.' + route
            # Return the new route appended to the current one.
            return self.route + route
        # We need to take a number of steps back from the
        # current route;
        else:
            # We'll need to trim the current route;
            # First, get it as a list;
            base_route_list = self.route.split('.')
            # Also if we are appending, put a dot in front of the new part;
            if route:
                route = '.' + route
            # If we arent reversing past the start of it;
            if back_counter < len(base_route_list):
                # Cut the right amount off, and stick the new route on;
                return '.'.join(base_route_list[0:-back_counter]) + route
            # We were reversing past the start, so just return
            # the root route, with the new bit stuck on;
            else:
                return self._root_route + route

    def _fetch_component_for_route(self, route: str) -> 'ConsoleAppComponent':
        component_name = self._route_component_maps[route]
        return self.fetch_component(component_name)

    def make_component(self, component_class_name: str) -> 'ConsoleAppComponent':
        '''Creates and returns a new instance of the component by finding its 
        constructor in the registered component packages.
        '''
        # Convert the class name into its corresponding filename;
        component_filename = pascal_to_snake(component_class_name)
        # Create place to put constructor when found;
        constructor = None
        # Then look in the default components;
        builtins_package = pcap.configs.builtin_component_package + '.{}'
        if util.find_spec(builtins_package.format(component_filename)):
            component_module = importlib.import_module(
                builtins_package.format(component_filename))
            constructor = getattr(component_module, component_class_name)
        # Still not found, so look in the registered component packages;
        for package_path in self._component_packages:
            if util.find_spec('{}.{}'.format(package_path, component_filename)):
                component_module = importlib.import_module('{}.{}'
                                                           .format(package_path, component_filename))
                constructor = getattr(component_module, component_class_name)
        # Raise an exception if still not found;
        if not constructor:
            raise ModuleNotFoundError('The component class {} was not found.'.
                                      format(component_class_name))
        # Instantiate the class and add it to the components dict;
        component: 'ConsoleAppComponent' = constructor(self)
        self._components[component_class_name] = component
        # Add the app reference to the component instance;
        component.app = self
        # Return the finished component;
        return component

    def fetch_component(self, component_instance_name: str) -> 'ConsoleAppComponent':
        '''Looks for the component in the loaded component cache first,
        and, if not found there, calls make_component to get a new instance.
        '''
        # Convert the instance name into the class name;
        component_class_name = snake_to_pascal(component_instance_name)
        # First look inside initialised components;
        if component_class_name in self._components.keys():
            return self._components[component_class_name]
        # Possibly not loaded yet, so make try make;
        return self.make_component(component_class_name)

    def register_component_package(self, package_path: str) -> None:
        '''Registers a dir as containing component files.

        Args:
            package_path (str): Path to dir containing files.
        '''
        self._component_packages.append(package_path)

    def register_component_packages(self, package_paths: List[str]) -> None:
        '''Registers a list of dirs as containing component files.

        Args:
            package_paths (List[str]): List of dirs containing component files.
        '''
        for path in package_paths:
            self.register_component_package(path)

    def activate_component(self, component_instance: 'ConsoleAppComponent') -> None:
        if not component_instance in self._active_components:
            self._active_components.append(component_instance)

    def _check_guards(self, route: str) -> None:
        '''Runs and collects response from any applicable guards.

        Args:
            route (List[str]): The current route.
        '''
        # Place to put matching guard component (if found);
        component = None
        # First check the exit guards;
        for guarded_route in self._route_exit_guard_map.keys():
            # If the guarded root does not feature in the submitted route;
            if not guarded_route in route:
                # The submitted route must have exited, so populate the component;
                component = self._route_exit_guard_map[guarded_route]
                # And don't look through any more exit guards;
                break
        # Now check the entrance guards;
        for guarded_route in self._route_entrance_guard_map.keys():
            # If the guarded root is part of the submitted route;
            if guarded_route in route:
                # Then the submitted route must be beyond the guard, so populate the
                # component;
                component = self._route_entrance_guard_map[guarded_route]
                # And don't look through any more entrance guards;
                break
        # If the guard component was populated, then use it;
        if component:
            self.clear_console()
            self._response = input(component.call_print())

    def guard_entrance(self, route: str, guard_component_class_name: str) -> None:
        # Interpret the route;
        route = self.interpret_relative_route(route)
        # Make a new guard instance;
        guard_component = cast(
            'ConsoleAppGuardComponent',
            self.make_component(guard_component_class_name)
        )
        self._route_entrance_guard_map[route] = guard_component

    def guard_exit(self, route: str, guard_component_class_name: str) -> None:
        # Interpret the route;
        route = self.interpret_relative_route(route)
        # Make a new guard instance;
        guard_component = cast(
            'ConsoleAppGuardComponent',
            self.make_component(guard_component_class_name)
        )
        self._route_exit_guard_map[route] = guard_component

    def clear_entrance(self, route: str) -> None:
        route = self.interpret_relative_route(route)
        if route in self._route_entrance_guard_map.keys():
            del self._route_entrance_guard_map[route]

    def clear_exit(self, route: str) -> None:
        route = self.interpret_relative_route(route)
        if route in self._route_exit_guard_map.keys():
            del self._route_exit_guard_map[route]

    def process_response(self, response: str) -> None:
        '''If the response is empty, iterates over active components
        calling for an available empty-responder. If not empty, first
        iterates over active components looking for a matching marker-responder,
        then iterates over active components looking for a markerless-responder.

        Args:
            response (str): The user's response.
        '''
        matched_responder = False
        try:
            # If the response is empty, give each active component a chance to respond;
            if response.replace(' ', '') == '':
                for component in self._active_components:
                    argless_responder = component.argless_responder
                    if argless_responder:
                        argless_responder()
                        matched_responder = True
                        if self._finished_responding: return
            
            # Otherwise, give any marker-only responders a chance;
            else:
                for component in self._active_components:
                    responders = component.marker_responders
                    if len(responders):
                        for responder in responders:
                            if responder.check_response_match(response):
                                responder(response)
                                matched_responder = True
                                if self._finished_responding: return
           
            # Finally give each active component a chance to field a
            # markerless responder;
            for component in self._active_components:
                markerless_responder = component.markerless_responder
                if markerless_responder:
                    markerless_responder(response)
                    matched_responder = True
                    if self._finished_responding: return
        
            # If no component has responded, then raise an exception;
            if not matched_responder and not response.replace(' ', '') == '': 
                raise ResponseValidationError('This response isn\'t recognised.')

        except pcap.ResponseValidationError as err:
            if err.message: self.error_message = err.message
            return

    def continue_responding(self) -> None:
        self._finished_responding = False

    def stop_responding(self) -> None:
        self._finished_responding = True

    def run(self) -> None:
        '''Main run loop for the CLI
        '''
        # Enter the main loop;
        while not self._quit:
            # If response has been collected;
            if not self._response == None:
                self.process_response(self._response)
                self._finished_responding = False
                self._response = None
            # If we are drawing the next view;
            else:
                self._active_components = []
                # Check guards;
                self._check_guards(self.route)
                # If no guards collected a response;
                if not self._response:
                    # Grab the matching component;
                    component = self._fetch_component_for_route(self.route)
                    # Call before print function;
                    component.before_print()
                    # Grab component again, in case before_print changed the route;
                    component = self._fetch_component_for_route(self.route)
                    # Clear the screen;
                    self.clear_console()
                    # Collect the output from the component's print response;
                    from_print = component.print()
                    # If there is no prefill;
                    if type(from_print) is str:
                        self._response = input(from_print)
                    # If there is prefill;
                    elif type(from_print) is tuple:
                        self._response = rlinput(from_print[0], from_print[1])

    def goto(self, route: str) -> None:
        # Convert the new route to be absolute;
        route = self.interpret_relative_route(route)
        # Save the current route to the history;
        self._route_history.append(self.route)
        # Make sure the history doesn't get too long;
        while len(self._route_history) > pcap.configs.route_history_length:
            self._route_history.pop(0)
        # Set the new route;
        self.route = route

    def back(self) -> None:
        self.route = self._route_history.pop()

    def clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def quit(self):
        self._quit = True
