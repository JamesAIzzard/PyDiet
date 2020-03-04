from typing import Any

class Injector():
    def __init__(self):
        pass
    
    def __setattr__(self, name: str, value: Any) -> None:
        setattr(self, name, value)

    def __getattribute__(self, name: str) -> Any:
        return getattr(self, name)

injector = Injector()
