import tkinter as tk
from typing import Optional

import gui


class View(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, **kwargs)

        self.columnconfigure(0, weight=1)  # Make the 0th col expand to fill full width of self.

        # Add the save and reset button to the top;
        self._save_reset_frame = tk.Frame(master=self)
        self.save_button = tk.Button(master=self._save_reset_frame, text="Save")
        self.save_button.bind("<Button-1>", lambda _: self.event_generate("<<save-clicked>>"))
        self.save_button.grid(row=0, column=0, padx=5)
        self.reset_button = tk.Button(master=self._save_reset_frame, text="Reset")
        self.reset_button.bind("<Button-1>", lambda _: self.event_generate("<<reset-clicked>>"))
        self.reset_button.grid(row=0, column=1, padx=5)
        self._save_reset_frame.grid(row=0, column=0, sticky="ew")

        # Basic info groups;
        self._basic_info_frame = tk.Frame(master=self)
        self.ingredient_name_widget = gui.labelled_entry.View(master=self._basic_info_frame,
                                                              label_text="Ingredient Name",
                                                              entry_width=40)
        self.ingredient_name_widget.grid(row=0, column=0)
        self._basic_info_frame.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

    def clear(self) -> None:
        """Clears the fields in the form."""
        self.ingredient_name_widget.clear()


class Controller(gui.ViewController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Bind the handlers;
        self._view.bind("<<save-clicked>>", self._on_save_clicked)
        self._view.bind("<<reset-clicked>>", self._on_reset_clicked)

    @property
    def ingredient_name(self) -> Optional[str]:
        """Gets the value from the ingredient name field."""
        return self._view.ingredient_name_widget.get()

    def _on_save_clicked(self, event) -> None:
        """Handler for ingredient save."""
        print("save ingredient clicked", self.ingredient_name)

    def _on_reset_clicked(self, event) -> None:
        """Handler for reset button."""
        self._view: 'View'  # Add specificity for intellisense;
        self._view.clear()
