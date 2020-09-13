from typing import Optional, Callable, TYPE_CHECKING

import pyconsoleapp
from pyconsoleapp import ConsoleAppComponent, builtin_validators, styles

from pydiet import cost, quantity

if TYPE_CHECKING:
    from pydiet.cost.supports_cost import SupportsCostSetting

_main_menu_template = '''
----------------|------------------
Save Changes    | -save
Reset           | -reset
----------------|------------------
Set Cost        | -cost [cost]
Set Qty         | -per  [quantity]
Set Units       | -unit [unit]
----------------|------------------

{def_qty}{def_unit} of {name} costs £{def_amount_cost} (£{cost_per_g} per g)
'''


class CostEditorComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self.subject: 'SupportsCostSetting'
        self.save_func: Callable
        self._ref_cost: Optional[float] = None

        self.configure_printer(self.print_main_menu_view)

        self.configure_responder(self.on_edit_cost, args=[
            self.configure_std_primary_arg(
                'cost', markers=['-cost'], validators=[self._validate_cost]),
            self.configure_std_option_arg('per', markers=[
                                          '-per'], validators=[builtin_validators.validate_positive_nonzero_number]),
            self.configure_std_option_arg('units', markers=[
                                          '-unit'], validators=[self._validate_units])
        ])

        self.configure_responder(self.on_edit_per, args=[
            self.configure_std_primary_arg('per', markers=[
                                           '-per'], validators=[builtin_validators.validate_positive_nonzero_number])
        ])

        self.configure_responder(self.on_edit_units, args=[
            self.configure_std_primary_arg('unit', markers=[
                                           '-unit'], validators=[self._validate_units])
        ])

        self.configure_responder(self.on_save, args=[
            self.configure_valueless_primary_arg('save', markers=['-save'])
        ])

        self.configure_responder(self.on_reset, args=[
            self.configure_valueless_primary_arg('reset', markers=['-reset'])
        ])

    def print_main_menu_view(self):
        # Init starting values;
        def_qty = '###'
        def_unit = '###'
        def_amount_cost = '#.##'
        cost_per_g = '#.##'

        # Update values where possible;
        if self.subject.cost_def_qty_defined:
            def_qty = self.subject.cost_def_qty
        if self.subject.cost_def_unit_defined:
            def_unit = self.subject.cost_def_unit_defined
        if not self.def_amount_cost == None:
            def_amount_cost = self._def_cost
        if self.subject.cost_fully_defined:
            cost_per_g = self.subject.cost_per_g

        # Build & return the template;
        output = _main_menu_template.format(
            def_qty=styles.fore(def_qty, 'blue'),
            def_unit=styles.fore(def_unit, 'blue'),
            name=self.subject.name,
            def_amount_cost=styles.fore(def_amount_cost, 'blue'),
            cost_per_g=styles.fore(cost_per_g, 'blue')
        )
        return self.app.fetch_component('standard_page_component').print(
            page_title='Cost Editor',
            page_content=output
        )

    def _validate_units(self, units: str) -> str:
        try:
            units = quantity.quantity_service.validate_qty_unit(units)
        except quantity.exceptions.UnknownUnitError:
            raise pyconsoleapp.ResponseValidationError(
                'The unit is not recognised.')
        if units in quantity.quantity_service.get_recognised_vol_units() and not self.subject.density_is_defined:
            raise pyconsoleapp.ResponseValidationError(
                'Density must be defined before volumetric units can be used.')
        elif units == quantity.supports_bulk.BulkTypes.PIECE and not self.subject.piece_mass_defined:
            raise pyconsoleapp.ResponseValidationError(
                'Piece mass must be defined before cost can be set per piece.')
        return units

    def _validate_cost(self, cost_value: float) -> float:
        try:
            cost_value = cost.cost_service.validate_cost(cost_value)
        except cost.exceptions.CostValueError:
            raise pyconsoleapp.ResponseValidationError(
                'The cost must be a positive number')
        return cost_value

    def _try_calculate_value(self) -> None:
        if not self._ref_cost == None and \
                self.subject.cost_def_qty_defined and \
                self.subject.cost_def_unit_defined:
            self.subject.set_cost(self._def_cost,
                                  self.subject.cost_def_qty,
                                  self.subject.cost_def_unit)

    def on_edit_cost(self, args) -> None:
        self._ref_cost = args['cost']

        # Set any optional args which went in;
        if not args['units'] == None:
            self.on_edit_units(args)
        if not args['per'] == None:
            self.on_edit_per(args)

        self._try_calculate_value()

    def on_edit_per(self, args) -> None:
        self.subject.set_cost_reference_qty(args['per'])
        self._try_calculate_value()

    def on_edit_units(self, args) -> None:

        def set_def_units(self, args):
            self.subject.set_pref_unit(args['unit'])
            self._try_calculate_value()

        def on_yes():
            self.subject.set_pref_unit(args['unit'])  # type: ignore
            set_def_units(self, args['unit'])

        def on_no():
            set_def_units(self, args['unit'])

        # Offer to update the overall pref unit if doesn't match;
        if not args['unit'] == self.subject.pref_units and \
                isinstance(self.subject, quantity.supports_bulk.SupportsBulkSetting):
            popup = pyconsoleapp.build_popup(
                message='Do you want to update the preferred bulk units to {}?'.format(
                    args['unit']),
                on_yes=on_yes,
                on_no=on_no
            )
            self.app.set_popup(popup)

    def on_save(self) -> None:
        self.save_func()

    def on_reset(self) -> None:
        self.subject.reset_cost_data()
        self._ref_cost = None
        self.app.info_message = 'Cost data reset.'
