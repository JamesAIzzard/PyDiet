import os
import importlib
import importlib.util
from typing import Callable, Dict, List, Optional, TYPE_CHECKING, cast

import pinjector
from pinjector import inject

from pyconsoleapp import utility_service
from pyconsoleapp import configs

if TYPE_CHECKING:
    from pyconsoleapp.console_app_component import ConsoleAppComponent
    from pyconsoleapp.console_app_guard_component import ConsoleAppGuardComponent

pinjector.create_namespace('pyconsoleapp')
pinjector.register('pyconsoleapp', utility_service)
pinjector.register('pyconsoleapp', configs)


class ConsoleApp():
    def __init__(self, name):
        self._ut: 'utility_service' = inject('pyconsoleapp.utility_service')
        self._cf: 'configs' = inject('pyconsoleapp.configs')
        self._response: Optional[str] = None
        self._root_route: str = ''
        self._route: str = ''
        self._route_component_maps: Dict[str, str] = {}
        self._route_exit_guard_map: Dict[str, 'ConsoleAppGuardComponent'] = {}
        self._route_entrance_guard_map: Dict[str,
                                             'ConsoleAppGuardComponent'] = {}
        self._components: Dict[str, 'ConsoleAppComponent'] = {}
        self._active_components: List['ConsoleAppComponent'] = []        
        self._component_packages: List[str] = []
        self._quit: bool = False
        self.name: str = name
        self.error_message: Optional[str] = None
        self.info_message: Optional[str] = None
        # Upload self to DI;
        pinjector.register('pyconsoleapp', self, 'app')

    @property
    def _active_option_responses(self) -> Dict[str, Callable]:
        '''Returns a dict of all currently active option responses.

        Returns:
            Dict[str, Callable]: A dict of all currently active option
            responses.
        '''
        # Collect the option responses map from each active component;
        option_responses = {}
        for component in self._active_components:
            option_responses.update(component.option_responses)
        # Then return them;
        return option_responses

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

    def _fetch_component_for_route(self, route: str) -> 'ConsoleAppComponent':
        component_name = self._route_component_maps[route]
        return self.fetch_component(component_name)

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
            self._response = input(component.print())

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

    def register_component_package(self, package_path: str) -> None:
        self._component_packages.append(package_path)

    def activate_component(self, component_instance:'ConsoleAppComponent') -> None:
        self._active_components.append(component_instance)

    def make_component(self, component_class_name: str) -> 'ConsoleAppComponent':
        # Convert the class name into its corresponding filename;
        component_filename = self._ut.pascal_to_snake(component_class_name)
        # Create place to put constructor when found;
        constructor = None
        # Then look in the default components;
        builtins_package = self._cf.builtin_component_package + '.{}'
        if importlib.util.find_spec(builtins_package.format(component_filename)):
            component_module = importlib.import_module(
                builtins_package.format(component_filename))
            constructor = getattr(component_module, component_class_name)
        # Still not found, so look in the registered component packages;
        for package_path in self._component_packages:
            if importlib.util.find_spec('{}.{}'.format(package_path, component_filename)):
                component_module = importlib.import_module('{}.{}'
                                                           .format(package_path, component_filename))
                constructor = getattr(component_module, component_class_name)
        # Raise an exception if still not found;
        if not constructor:
            raise ModuleNotFoundError('The component class {} was not found.'.
                                      format(component_class_name))
        # Instantiate the class and add it to the components dict;
        component: 'ConsoleAppComponent' = constructor()
        self._components[component_class_name] = component
        # Add the app reference to the component instance;
        component.app = self
        # Return the finished component;
        return component

    def fetch_component(self, component_instance_name: str) -> 'ConsoleAppComponent':
        # First look inside initialised components;
        if component_instance_name in self._components.keys():
            return self._components[component_instance_name]
        # Possibly not loaded yet, so make try make;
        # Make the instance name into a class name;
        component_class_name = self._ut.snake_to_pascal(
            component_instance_name)
        return self.make_component(component_class_name)

    def root_route(self, route: str, component_class_name: str) -> None:
        self._root_route = route
        self.add_route(route, component_class_name)

    def add_route(self, route: str, component_class_name: str) -> None:
        self._route_component_maps[route] = \
            self._ut.pascal_to_snake(component_class_name)

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

    def process_response(self, response):
        '''First runs any matching active option responses. Then runs
        all active dynamic responses.

        Args:
            response (str): The user's response.
        '''
        # Collect the currently active option responses;
        active_option_responses = self._active_option_responses
        # If the response matches any static options;
        if response in active_option_responses.keys():
            active_option_responses[response]()
        # If not, run the dynamic responses;
        else:
            for component in self._active_components:
                component.dynamic_response(response)

    def run(self) -> None:
        '''Main run loop for the CLI
        '''
        # Enter the main loop;
        while not self._quit:
            # If response has been collected;
            if self._response:
                self.process_response(self._response)
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
                    # Call run;
                    component.run()
                    # Grab component again, in case run changed the route;
                    component = self._fetch_component_for_route(self.route)
                    # Print the view and collect response;
                    self.clear_console()
                    self._response = input(component.print())

    def goto(self, route: str) -> None:
        # Convert the route to be absolute;
        route = self.interpret_relative_route(route)
        # Set the route;
        self.route = route

    def clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def quit(self):
        self._quit = True
