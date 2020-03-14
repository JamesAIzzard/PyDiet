from typing import Any

class Injector():
    def __init__(self):
        self._dependencies = {}
    
    def register(self, dependency_class:Any)->None:
        self._dependencies[dependency_class.__name__] = {}
        self._dependencies[dependency_class.__name__]['class'] = dependency_class
        self._dependencies[dependency_class.__name__]['instance'] = None

    def inject(self, dependency_name:str)->Any:
        if self._dependencies[dependency_name]['instance']:
            return self._dependencies[dependency_name]['instance']
        else:
            self._dependencies[dependency_name]['instance'] = \
                self._dependencies[dependency_name]['class']()
            return self._dependencies[dependency_name]['instance']


injector = Injector()
