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

{name} costs £{ref_cost} per {ref_qty}{ref_unit} (£{cost_per_g} per g)
'''

# -cost 12.00 -per 100 -unit g
# -cost 12.00
# -per 100
# -unit g


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

    def print_main_menu_view(self):
        ref_cost = '#.##'
        ref_qty = '###'
        ref_unit = '##'
        cost_per_g = '#.##'
        if not self._ref_cost == None:
            ref_cost = format(self._ref_cost, '.2f')
        if self.subject.cost_ref_qty_defined:
            ref_qty = format(self.subject.cost_ref_qty, '.2f')
        if self.subject.cost_ref_units_defined:
            ref_unit = self.subject.cost_ref_units
        if self.subject.cost_per_g_defined:
            cost_per_g = format(self.subject.cost_per_g, '.2f')
        output = _main_menu_template.format(
            name=self.subject.name,
            ref_cost=styles.fore(ref_cost, 'blue'),
            ref_qty=styles.fore(ref_qty, 'blue'),
            ref_unit=styles.fore(ref_unit, 'blue'),
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
            raise pyconsoleapp.ResponseValidationError('The unit is not recognised.')
        if units in quantity.quantity_service.get_recognised_vol_units() and not self.subject.density_is_defined:
            raise pyconsoleapp.ResponseValidationError(
                'Density must be defined before volumetric units can be used.')
        elif units == quantity.supports_bulk.BulkTypes.PIECE and not self.subject.piece_mass_defined:
            raise pyconsoleapp.ResponseValidationError(
                'Piece mass must be defined before cost can be set per piece.')
        return units

    def _validate_cost(self, cost_value:float) -> float:
        try:
            cost_value = cost.cost_service.validate_cost(cost_value)
        except cost.exceptions.InvalidCostValueError:
            raise pyconsoleapp.ResponseValidationError('The cost must be a positive number')
        return cost_value

    def _calculate(self) -> None:
        if not self._ref_cost == None and \
                self.subject.cost_ref_units_defined and \
                self.subject.cost_ref_qty_defined:
            cost_per_pref_unit = self._ref_cost/self.subject.cost_ref_qty
            k = self.subject.grams_to_other_units_ratio(
                self.subject.cost_ref_units)
            cost_per_g = cost_per_pref_unit*k
            self.subject.set_cost_per_g(cost_per_g)

    def on_edit_cost(self, args) -> None:
        self._ref_cost = args['cost']

        # Set any optional args which went in;
        if not args['units'] == None:
            self.subject.set_cost_ref_units(args['units'])
        if not args['per'] == None:
            self.subject.set_cost_ref_qty(args['per'])

        # Try complete the cost_per_g calc;
        self._calculate()

    def on_edit_per(self, args) -> None:
        self.subject.set_cost_ref_qty(args['per'])
        self._calculate()

    def on_edit_units(self, args) -> None:
        self.subject.set_cost_ref_units(args['unit'])
        self._calculate()

    def on_save(self) -> None:
        self.save_func()
