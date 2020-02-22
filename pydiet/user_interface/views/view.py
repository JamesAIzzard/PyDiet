import os


class View:
    def __init__(self):
        self.text = None

    def _startup_action(self):
        pass

    def response_action(self, res):
        raise NotImplementedError

    def show(self):
        self._startup_action()
        return input(self.text)

