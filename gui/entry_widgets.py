import tkinter as tk
from typing import Optional


class SmartEntryWidget(tk.Entry):
    def __init__(self, width: int = 10, valid_bg: str = "#FFFFFF",
                 invalid_bg: str = "#D7806D", **kwargs):
        self._value = tk.StringVar()  # Shim in textvar so we can watch for value changes;
        super().__init__(width=width, textvariable=self._value, bg=valid_bg, **kwargs)
        # Stash the valid/invalid background colours;
        self._valid_bg = valid_bg
        self._invalid_bg = invalid_bg
        self._valid: bool = True  # Init the validity tracker.

        # Raise event when value changes;
        self._value.trace_add("write", callback=lambda *args: self.event_generate("<<Value-Changed>>"))

    def set(self, value: str) -> None:
        """Sets the widget's value."""
        self._value.set(value)  # Using the value var triggers the change event.

    def clear(self) -> None:
        """Clears the textbox."""
        self._value.set("")  # Using the value var triggers the change event.

    @property
    def in_valid_state(self) -> bool:
        """Returns True/False to indicate if widget is in invalid state."""
        return self._valid

    @property
    def in_invalid_state(self) -> bool:
        """Returns True/False to indicate if widget is in an invalid state."""
        return not self._valid

    def make_invalid(self) -> None:
        """Sets the textbox to its invalid state."""
        self.configure(bg=self._invalid_bg)
        self._valid = False

    def make_valid(self) -> None:
        """Sets the textbox to its valid state."""
        self.configure(bg=self._valid_bg)
        self._valid = True


class LabelledEntryWidget(tk.Frame):
    def __init__(self, label_text: str = "", entry_width: int = 10,
                 invalid_bg: str = "#D7806D", **kwargs):
        super().__init__(**kwargs)
        self._label = tk.Label(master=self, text=label_text)
        self._entry = SmartEntryWidget(master=self, width=entry_width, invalid_bg=invalid_bg)
        self._label.grid(row=0, column=0)
        self._entry.grid(row=0, column=1)

        # Forward the value changed event;
        self._entry.bind("<<Value-Changed>>", lambda _: self.event_generate("<<Value-Changed>>"))

    def get(self) -> Optional[str]:
        """Returns the text content of the entry element."""
        return self._entry.get()

    def set(self, value: str) -> None:
        """Sets the text content of the entry element."""
        self._entry.set(value)

    def clear(self) -> None:
        """Clears the textbox."""
        self._entry.clear()

    def make_invalid(self) -> None:
        """Sets the textbox to valid."""
        self._entry.make_invalid()

    def make_valid(self) -> None:
        """Sets the textbox to invalid."""
        self._entry.make_valid()
