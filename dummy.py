from typing import Union, Any

class A():
    def __init__(self):
        pass

class B(A):
    def __init__(self):
        self.text:str
    def print(self):
        print(self.text)

def get_instance():
    return B()

i1:'B' = get_instance() # Pyright error here
i1.text = 'hello'
i2:'A' = get_instance()

