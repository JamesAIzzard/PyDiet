from typing import Optional

import gui
import model


def set_noneable_qty_entry(entry_widget: 'gui.SmartEntryWidget', qty_value: Optional[float]):
    """Sets the value of the entry widget to reflect the value submitted.
    - If the value is None, the entry widget is set to and empty string.
    - If the value is a float, it is converted to a string and written to the entry widget.
    """
    if qty_value is None:
        qty_value = ""
    else:
        qty_value = str(model.quantity.validation.validate_quantity(qty_value))
    entry_widget.set(qty_value)


def get_noneable_qty_entry(entry_widget: 'gui.SmartEntryWidget') -> Optional[float]:
    """Gets the value the entry widget.
    - If the widget is empty, returns None.
    - If the widget is populated, converts to float and returns value.
    """
    if entry_widget.get().replace(" ", "") == "":
        return None
    else:
        return float(entry_widget.get())


def validate_qty_entry(entry_widget: 'gui.SmartEntryWidget') -> None:
    value = entry_widget.get()
    if not value == "":
        try:
            _ = model.quantity.validation.validate_quantity(float(value))
            entry_widget.make_valid()
        except (ValueError, model.quantity.exceptions.InvalidQtyError):
            entry_widget.make_invalid()
