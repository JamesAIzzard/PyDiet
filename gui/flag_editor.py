import tkinter as tk
from typing import Dict, Callable, Optional

import gui
import model


class FlagEditorView(tk.LabelFrame):
    def __init__(self, **kwargs):
        super().__init__(text="Flags", **kwargs)
        self.flags: Dict[str, 'gui.SmartDropdownWidget'] = {}

    def add_flag(self, flag_name: str, flag_label: str) -> None:
        """Adds a flag checkbox to the display."""
        # Make sure we aren't doubling up on a flag;
        if flag_name in self.flags.keys():
            raise ValueError("Can't add two flags with the same name.")
        label = tk.Label(master=self, text=flag_label)
        self.flags[flag_name] = gui.SmartDropdownWidget(master=self, width=9, values=["True", "False", "Undefined"])
        self.flags[flag_name].set("Undefined")
        label.grid(row=len(self.flags), column=0, sticky="w")
        self.flags[flag_name].grid(row=len(self.flags), column=1, sticky="w")

    def remove_all_flags(self) -> None:
        """Remove all flag elements from the UI."""
        self.flags = {}  # Wipe the dict.
        for child in self.winfo_children():  # Sweep the frame.
            child.destroy()

    def set_flag_value(self, flag_name: str, flag_value: Optional[bool]) -> None:
        """Sets the flag checkbox to a specific state."""
        # Note: Since we are specialising the SmartDropdown widget, its OK to specialise the I/O to booleans here.
        # Check the flag value is recognised;
        if flag_value not in [True, False, None]:
            raise ValueError(f"{flag_value} is not a recognised flag value.")
        # Check the flag name is recognised;
        if flag_name not in self.flags.keys():
            raise ValueError(f"The flag: {flag_name} was not found.")
        # Convert the optional boolean into a string;
        if flag_value is None:
            self.flags[flag_name].set("Undefined")
        elif flag_value is True:
            self.flags[flag_name].set("True")
        elif flag_value is False:
            self.flags[flag_name].set("False")

    def get_flag_value(self, flag_name: str) -> Optional[bool]:
        """Returns the state of the named flag."""
        # Note: Since we are specialising the SmartDropdown widget, its OK to specialise the I/O to booleans here.

        # Check the flag name is recognised;
        if flag_name not in self.flags.keys():
            raise ValueError(f"The flag: {flag_name} was not found.")
        # Convert the string value back into boolean;
        if self.flags[flag_name].get() == "Undefined":
            return None
        elif self.flags[flag_name].get() == "True":
            return True
        elif self.flags[flag_name].get() == "False":
            return False
        else:
            raise ValueError(f"Unrecognised flag value {self.flags[flag_name].get()}")


class FlagEditorController(gui.HasSubject):
    def __init__(self, view: 'FlagEditorView', on_flag_value_change_callback: Callable[..., None], **kwargs):
        super().__init__(subject_type=model.quantity.HasSettableBulk, view=view, **kwargs)
        self._on_flag_value_change_callback = on_flag_value_change_callback
        # Populate with the system flags;
        for flag_name in model.flags.all_flag_names():
            self.view.add_flag(
                flag_name=flag_name,
                flag_label=f"{flag_name.replace('_', ' ')}: "
            )
            self.view.flags[flag_name].bind("<<Value-Changed>>", on_flag_value_change_callback)

    @property
    def flag_values(self) -> Dict[str, Optional[bool]]:
        """Returns the flag values from the form."""
        values: Dict[str, Optional[bool]] = {}
        for flag_name, str_value in self.view.flags.items():
            values[flag_name] = self.view.get_flag_value(flag_name)
        return values

    def get_flag_value(self, flag_name: str) -> Optional[bool]:
        """Gets the value of a flag by name."""
        return self.view.get_flag_value(flag_name)

    def set_flag_value(self, flag_name: str, flag_value=Optional[bool]):
        """Sets the value of a flag by name."""
        self.view.set_flag_value(flag_name, flag_value)

    @property
    def subject(self) -> 'model.flags.HasSettableFlags':
        return super().subject

    def set_subject(self, subject: 'model.flags.HasSettableFlags') -> None:
        super().set_subject(subject)

    @property
    def view(self) -> 'FlagEditorView':
        return super().view

    def update_view(self) -> None:
        for flag_name in self.view.flags.keys():
            self.set_flag_value(flag_name, self.subject.get_flag_value(flag_name))

    def process_view_changes(self, flag_name: str, *args, **kwargs) -> None:
        pass
