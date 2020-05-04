from typing import Any, Dict
import re

__ioc_containers: Dict[str, 'IOCContainer'] = {}


def pascal_to_snake(text: str) -> str:
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def create_namespace(namespace: str) -> None:
    # Check if the namespace exists already;
    if namespace in __ioc_containers.keys():
        raise ValueError('A DI namespace called {} has been created already.'
                         .format(namespace))
    __ioc_containers[namespace] = IOCContainer()


def register(namespace: str, dependency: Any, alias: str = None) -> None:
    # If a constructor has been registered;
    if dependency.__class__.__name__ == 'type':
        if not alias:
            alias = pascal_to_snake(dependency.__name__)
        __ioc_containers[namespace]._constructors[alias] = dependency
    # If a module has been registered;
    elif dependency.__class__.__name__ == 'module':
        if not alias:
            alias = pascal_to_snake(dependency.__name__.split('.')[-1])
        __ioc_containers[namespace]._container[alias] = dependency
    # If a type instance has been registered;
    else:
        if not alias:
            alias = pascal_to_snake(dependency.__class__.__name__)
        __ioc_containers[namespace]._container[alias] = dependency


def inject(namespace_dot_name: str) -> Any:
    # Split the namespace from the dependency name;
    namespace = '.'.join(namespace_dot_name.split('.')[:-1])
    name = namespace_dot_name.split('.')[-1]
    # Raise an exception if the namespace doesn't exist;
    if not namespace in __ioc_containers.keys():
        raise KeyError('The namespace {} was not found in the DI container.'.format(namespace))
    # Get the right IOC container;
    iocc: 'IOCContainer' = __ioc_containers[namespace]
    # Raise an exception if the name doesn't exist in the container;
    if not name in iocc._constructors.keys() and not name in iocc._container.keys():
        raise KeyError(
            'The dependency {} was not found in the {} namespace.'.format(name, namespace))
    # If the instance is already in the ioc container,
    # then return it;
    if name in iocc._container.keys():
        return iocc._container[name]
    # Otherwise, instantiate it first and then return it;
    else:
        iocc._container[name] = iocc._constructors[name]()
        return iocc._container[name]


class IOCContainer():
    def __init__(self):
        self._container: Dict[str, Any] = {}
        self._constructors: Dict[str, Any] = {}
