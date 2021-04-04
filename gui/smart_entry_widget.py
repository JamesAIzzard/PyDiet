import tkinter as tk


class SmartEntryWidget(tk.Entry):
    def __init__(self, width: int = 10, valid_bg: str = "#FFFFFF",
                 invalid_bg: str = "#D7806D", **kwargs):
        self._value = tk.StringVar()  # Shim in textvar so we can watch for value changes;
        super().__init__(width=width, textvariable=self._value, bg=valid_bg, **kwargs)
        self._valid_bg = valid_bg
        self._invalid_bg = invalid_bg
        self._valid: bool = True

        # Raise event when value changes;
        self._value.trace_add("write", callback=lambda *args: self.event_generate("<<Value-Changed>>"))

    def clear(self) -> None:
        """Clears the textbox."""
        self.delete("0", tk.END)

    @property
    def in_invalid_state(self) -> bool:
        """Returns True/False to indicate if widget is in invalid state."""
        return self._valid

    def make_invalid(self):
        """Sets the textbox to its invalid state."""
        self.config(bg=self._invalid_bg)
        self._valid = False

    def make_valid(self):
        """Sets the textbox to its valid state."""
        self.config(bg=self._valid_bg)
        self._valid = True
