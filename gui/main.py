import tkinter as tk
from typing import Optional

import gui

class App:
    """PyDiet application."""

    def __init__(self):
        self._root = tk.Tk()
        self._root.title("PyDiet")
        self._root.geometry("{}x{}".format(gui.configs.app_window_width, gui.configs.app_widow_height))
        self._root.iconbitmap("gui/assets/pydiet.ico")

        self.top_menu_view = gui.top_menu_widget.View(root=self._root)
        self.top_menu_controller = gui.top_menu_widget.Controller(app=self, view=self.top_menu_view)

        self.current_view: Optional['tk.Frame'] = None

    @property
    def root(self) -> 'tk.Tk':
        """Returns the top level app window object."""
        return self._root

    def draw(self) -> None:
        """Draws the main application in its current state."""

    def run(self) -> None:
        """Runs the app."""
        self._root.mainloop()
