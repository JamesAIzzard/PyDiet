class Services():
    def __init__(self):
        self._services = {}

    def __getattr__(self, name):
        return self._services[name]

    def add(self, service_name: str, service: object) -> None:
        self._services[service_name] = service

services = Services()