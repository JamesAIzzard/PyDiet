import tkinter as tk

import gui


class DensityEditorWidget(tk.Frame):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Build the UI elements;
        self._vol_value_and_unit = gui.EntryDropdownWidget(
            master=self,
            entry_width=10,
            invalid_bg=gui.configs.invalid_bg_colour,
            dropdown_width=5
        )
        self._vol_value_and_unit.grid(row=0, column=0)
        self._label = tk.Label(master=self, text=" weighs ")
        self._label.grid(row=0, column=1)
        self._mass_value_and_unit = gui.EntryDropdownWidget(
            master=self,
            entry_width=10,
            invalid_bg=gui.configs.invalid_bg_colour,
            dropdown_width=5
        )
        self._mass_value_and_unit.grid(row=0, column=2)

        # Bind events;
        self._vol_value_and_unit.bind("<<Entry-Value-Changed>>",
                                      lambda _: self.event_generate("<<Vol-Value-Changed>>"))
        self._vol_value_and_unit.bind("<<Dropdown-Value-Changed>>",
                                      lambda _: self.event_generate("<<Vol-Unit-Changed>>"))
        self._mass_value_and_unit.bind("<<Entry-Value-Changed>>",
                                       lambda _: self.event_generate("<<Mass-Value-Changed>>"))
        self._mass_value_and_unit.bind("<<Dropdown-Value-Changed>>",
                                       lambda _: self.event_generate("<<Mass-Unit-Changed>>"))


class PieceMassEditorWidget(tk.Frame):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Build the UI elements;
        self._num_pieces = gui.SmartEntryWidget(
            master=self,
            width=10,
            invalid_bg=gui.configs.invalid_bg_colour
        )
        self._num_pieces.grid(row=0, column=0)
        self._label = tk.Label(master=self, text=" piece(s) weighs ")
        self._label.grid(row=0, column=1)
        self._pieces_mass = gui.EntryDropdownWidget(
            master=self,
            entry_width=10,
            invalid_bg=gui.configs.invalid_bg_colour,
            dropdown_width=5
        )
        self._pieces_mass.grid(row=0, column=2)

        # Bind events;
        self._num_pieces.bind("<<Value-Changed>>", lambda _: self.event_generate("<<Num-Pieces-Changed"))
        self._pieces_mass.bind("<<Entry-Value-Changed>>", lambda _: self.event_generate("<<Mass-Value-Changed"))
        self._pieces_mass.bind("<<Dropdown-Value-Changed>>", lambda _: self.event_generate("<<Mass-Unit-Changed"))


class BulkEditorWidget(tk.LabelFrame):
    def __init__(self, **kwargs):
        super().__init__(text="Bulk Properties", **kwargs)
        self._ref_qty_and_unit_entry = gui.LabelledEntryDropdownWidget(
            master=self,
            label_text="Reference Quantity: ",
            entry_width=10,
            dropdown_width=5,
            invalid_bg=gui.configs.invalid_bg_colour,
        )
        self._density_entry = DensityEditorWidget(master=self)
        self._pc_mass_entry = PieceMassEditorWidget(master=self)
        self._ref_qty_and_unit_entry.grid(row=0, column=0, sticky="w")
        self._density_entry.grid(row=1, column=0, sticky="w")
        self._pc_mass_entry.grid(row=2, column=0, sticky="w")

        # Bind to child events and raise from top level widget;
        self._ref_qty_and_unit_entry.bind("<<Entry-Value-Changed>>",
                                          lambda _: self.event_generate("<<Ref-Qty-Value-Changed>>"))
        self._ref_qty_and_unit_entry.bind("<<Dropdown-Value-Changed>>",
                                          lambda _: self.event_generate("<<Ref-Qty-Unit-Changed>>"))
        self._density_entry.bind("<<Mass-Value-Changed>>",
                                 lambda _: self.event_generate("<<Density-Mass-Value-Changed>>"))
        self._density_entry.bind("<<Mass-Unit-Changed>>",
                                 lambda _: self.event_generate("<<Density-Mass-Unit-Changed>>"))
        self._density_entry.bind("<<Vol-Value-Changed>>",
                                 lambda _: self.event_generate("<<Density-Vol-Value-Changed>>"))
        self._density_entry.bind("<<Vol-Unit-Changed>>",
                                 lambda _: self.event_generate("<<Density-Vol-Unit-Changed>>"))
        self._pc_mass_entry.bind("<<Num-Pieces-Changed>>", lambda _: self.event_generate("<<Num-Pieces-Changed>>"))
        self._pc_mass_entry.bind("<<Mass-Value-Changed>>",
                                 lambda _: self.event_generate("<<Pieces-Mass-Value-Changed>>"))
        self._pc_mass_entry.bind("<<Mass-Unit-Changed>>", lambda _: self.event_generate("<<Pieces-Mass-Unit-Changed>>"))


class HasBulkEditorWidget(gui.HasSubject):
    def __init__(self, bulk_editor_widget: 'gui.BulkEditorWidget', **kwargs):
        super().__init__(**kwargs)
        self._bulk_editor_widget = bulk_editor_widget

        # Bind handlers to events;
        # todo ...

    def _on_ref_qty_value_change(self, _) -> None:
        """Handles changes to the reference quantity value."""

    def _on_ref_qty_unit_change(self, _) -> None:
        """Handles changes to the reference quantity unit."""

    def _on_density_mass_value_change(self, _) -> None:
        """Handles changes to the density mass value."""

    def _on_density_mass_unit_change(self, _) -> None:
        """Handles changes to the density mass unit."""

    def _on_density_vol_value_change(self, _) -> None:
        """Handles changes to the density volume value."""

    def _on_density_vol_unit_change(self, _) -> None:
        """Handles changes to the density volume unit."""

    def _on_piece_value_change(self, _) -> None:
        """Handles changes to the peice value."""

    def _on_piece_mass_value_change(self, _) -> None:
        """Handles changes to the piece mass value."""

    def _on_piece_mass_unit_change(self, _) -> None:
        """Handles changes to the piece mass unit."""
