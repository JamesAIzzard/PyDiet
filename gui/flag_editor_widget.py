import tkinter as tk
from typing import Dict, Optional

import gui
import model


class FlagEditorWidget(tk.Frame):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._flags: Dict[str, 'gui.LabelledDropdownWidget'] = {}

    def add_flag(self, flag_name: str, flag_label: str, flag_value: Optional[bool]) -> None:
        """Adds a flag checkbox to the display."""
        # Make sure we aren't doubling up on a flag;
        if flag_name in self._flags.keys():
            raise ValueError("Can't add two flags with the same name.")
        # Create the flag variable;
        self._flags[flag_name] = gui.LabelledDropdownWidget(
            master=self,
            label_text=flag_label,
            dropdown_width=10,
            values=["True", "False", "Undefined"]
        )
        # Init its value to Undefined;
        self._flags[flag_name].set("Undefined")
        # Add it to the UI;
        self._flags[flag_name].grid(row=len(self._flags), column=0, sticky="w")

    def remove_all_flags(self) -> None:
        """Remove all flag elements from the UI."""
        for child in self.winfo_children():
            child.destroy()

    def set_flag(self, flag_name: str, flag_value: Optional[bool]) -> None:
        """Sets the flag checkbox to a specific state."""
        # Check the flag value is recognised;
        if flag_value not in ["Undefined", "True", "False"]:
            raise ValueError(f"{flag_value} is not a recognised flag value.")
        # Check the flag name is recognised;
        if flag_name not in self._flags.keys():
            raise ValueError(f"The flag: {flag_name} was not found.")
        # Convert the optional boolean into a string;
        if flag_value is None:
            value = "Undefined"
        else:
            value = str(flag_value)
        self._flags[flag_name].set(value)

    def get_flag(self, flag_name) -> Optional[bool]:
        """Returns the state of the named flag."""
        # Check the flag name is recognised;
        if flag_name not in self._flags.keys():
            raise ValueError(f"The flag: {flag_name} was not found.")
        # Convert the string value back into boolean;
        if self._flags[flag_name].get() == "Undefined":
            return None
        else:
            return bool(self._flags[flag_name])


class FlagEditorController:
    def __init__(self, app: 'gui.App', view: 'FlagEditorWidget'):
        self._app = app
        self._view = view
        self._subject: Optional['model.flags.HasSettableFlags'] = None

    @property
    def subject(self) -> Optional['model.flags.HasSettableFlags']:
        """Gets the subject."""
        return self._subject

    @subject.setter
    def subject(self, subject:Optional['model.flags.HasSettableFlags']) -> None:
        """Sets the subject."""
        # Check the subject is the right type;
        if not isinstance(subject, model.flags.HasSettableFlags):
            raise TypeError("Subject must subclass HasSettableFlags.")
        # Set the subject;
        self._subject = subject
        # Update the UI to match the subject;
        self._view.remove_all_flags()
        for flag_name, flag_value in self._subject.all_flag_values.items():
            self._view.add_flag(flag_name, flag_name, flag_value)