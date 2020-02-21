import os


class View:
    def __init__(self):
        self.text = None

    def run(self):
        raise NotImplementedError

    def action(self, choice):
        pass
