import tkinter as tk

import gui


class ViewController:
    def __init__(self, app: 'gui.App', view: 'tk.Widget'):
        self._app = app
        self._view = view
