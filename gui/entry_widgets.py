import tkinter as tk


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
