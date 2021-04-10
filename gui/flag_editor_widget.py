import tkinter as tk
from typing import Dict, Optional

import gui
import model


class FlagEditorWidget(tk.LabelFrame):
    def __init__(self, **kwargs):
        super().__init__(text="Flags", **kwargs)
        self._flags: Dict[str, 'gui.SmartDropdownWidget'] = {}

    def add_flag(self, flag_name: str, flag_label: str) -> None:
        """Adds a flag checkbox to the display."""
        # Make sure we aren't doubling up on a flag;
        if flag_name in self._flags.keys():
            raise ValueError("Can't add two flags with the same name.")
        label = tk.Label(master=self, text=flag_label)
        self._flags[flag_name] = gui.SmartDropdownWidget(master=self, width=9, values=["True", "False", "Undefined"])
        self._flags[flag_name].set("Undefined")
        label.grid(row=len(self._flags), column=0, sticky="w")
        self._flags[flag_name].grid(row=len(self._flags), column=1, sticky="w")

    def remove_all_flags(self) -> None:
        """Remove all flag elements from the UI."""
        self._flags = {}  # Wipe the dict.
        for child in self.winfo_children():  # Sweep the frame.
            child.destroy()

    def set_flag(self, flag_name: str, flag_value: Optional[bool]) -> None:
        """Sets the flag checkbox to a specific state."""
        # Note: Since we are specialising the SmartDropdown widget, its OK to specialise the I/O to booleans here.
        # Check the flag value is recognised;
        if flag_value not in [True, False, None]:
            raise ValueError(f"{flag_value} is not a recognised flag value.")
        # Check the flag name is recognised;
        if flag_name not in self._flags.keys():
            raise ValueError(f"The flag: {flag_name} was not found.")
        # Convert the optional boolean into a string;
        if flag_value is None:
            self._flags[flag_name].set("Undefined")
        elif flag_value is True:
            self._flags[flag_name].set("True")
        elif flag_value is False:
            self._flags[flag_name].set("False")

    def get_flag(self, flag_name: str) -> Optional[bool]:
        """Returns the state of the named flag."""
        # Note: Since we are specialising the SmartDropdown widget, its OK to specialise the I/O to booleans here.

        # Check the flag name is recognised;
        if flag_name not in self._flags.keys():
            raise ValueError(f"The flag: {flag_name} was not found.")
        # Convert the string value back into boolean;
        if self._flags[flag_name].get() == "Undefined":
            return None
        elif self._flags[flag_name].get() == "True":
            return True
        elif self._flags[flag_name].get() == "False":
            return False
        else:
            raise ValueError(f"Unrecognised flag value {self._flags[flag_name].get()}")


class HasFlagEditorWidget(gui.HasSubject):
    def __init__(self, flag_editor_widget: 'FlagEditorWidget', **kwargs):
        super().__init__(**kwargs)

        # Check the subject has editable flags;
        if not issubclass(self.subject_type, model.flags.HasSettableFlags):
            raise TypeError("FlagEditorWidget requires the subject to support flag setting.")

        # Stash the flag editor widget;
        self._flag_editor_widget = flag_editor_widget

        # Use the model subject to add and set the required flag widgets;
        for flag_name in model.flags.all_flag_names():
            self._flag_editor_widget.add_flag(
                flag_name=flag_name,
                flag_label=flag_name.replace("_", " ")
            )

    @gui.HasSubject.subject.setter
    def subject(self, subject: 'model.flags.HasSettableFlags') -> None:
        # Pass subject to parent class first;
        super()._set_subject(subject)
        # Use subject to set flag values;
        for flag_name, flag_value in subject.all_flag_values.items():
            self._flag_editor_widget.set_flag(
                flag_name=flag_name,
                flag_value=flag_value
            )