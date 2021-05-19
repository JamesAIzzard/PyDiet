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
        qty_value = str(model.quantity.validation.validate_quantity(round(qty_value, 4)))
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


def entry_is_defined(entry_widget: 'gui.SmartEntryWidget') -> bool:
    """Returns True/False to indicate if there is a value in the entry widget."""
    return not entry_widget.get().replace(" ", "") == ""


def validate_qty_entry(entry_widget: 'gui.SmartEntryWidget') -> None:
    value = entry_widget.get()
    if not value == "":
        try:
            _ = model.quantity.validation.validate_quantity(float(value))
            entry_widget.make_valid()
        except (ValueError, model.quantity.exceptions.InvalidQtyError):
            entry_widget.make_invalid()
    if value.replace(" ", "") == "":
        entry_widget.make_valid()


def validate_nonzero_qty_entry(entry_widget: 'gui.SmartEntryWidget') -> None:
    validate_qty_entry(entry_widget)
    if entry_widget.is_valid and not entry_widget.get() == "":
        try:
            _ = model.quantity.validation.validate_nonzero_quantity(float(entry_widget.get()))
            entry_widget.make_valid()
        except model.quantity.exceptions.ZeroQtyError:
            entry_widget.make_invalid()


def configure_qty_units(dropdown: 'gui.SmartDropdownWidget', subject: 'model.quantity.HasBulk') -> None:
    """Configures the dropdown widget to match the subject's configured units."""
    # Save the old value;
    prev_value = dropdown.get()
    # Clear it all out;
    dropdown.remove_options()
    # Repopulate with correct options;
    dropdown.add_options(model.quantity.get_recognised_mass_units())
    if subject.density_is_defined:
        dropdown.add_options(model.quantity.get_recognised_vol_units())
    if subject.piece_mass_is_defined:
        dropdown.add_options(model.quantity.get_recognised_pc_units())
    # Reinstate the old value if it is still available;
    if prev_value in dropdown['values']:
        dropdown.set(prev_value)
