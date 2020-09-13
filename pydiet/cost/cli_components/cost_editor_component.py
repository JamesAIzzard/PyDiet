from typing import Optional, Callable, TYPE_CHECKING

import pyconsoleapp
from pyconsoleapp import ConsoleAppComponent, builtin_validators, styles

from pydiet import cost, quantity

if TYPE_CHECKING:
    from pydiet.cost.supports_cost import SupportsCostSetting

_main_menu_template = '''
----------------|------------------------------------------
Save Changes    | -save
Reset           | -reset
----------------|------------------------------------------
Set Cost        | -cost [cost] -per [quantity] -unit [unit]
----------------|------------------------------------------

Cost: {cost_summary}

'''


class CostEditorComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self.subject: 'SupportsCostSetting'
        self.save_func: Callable

        self.configure_printer(self.print_main_menu_view)

        self.configure_responder(self.on_edit_cost, args=[
            self.configure_std_primary_arg(
                'cost', markers=['-cost'], validators=[self._validate_cost]),
            self.configure_std_primary_arg('per', markers=[
                                          '-per'], validators=[builtin_validators.validate_positive_nonzero_number]),
            self.configure_std_primary_arg('units', markers=[
                                          '-unit'], validators=[self._validate_units])
        ])

        self.configure_responder(self.on_save, args=[
            self.configure_valueless_primary_arg('save', markers=['-save'])
        ])

        self.configure_responder(self.on_reset, args=[
            self.configure_valueless_primary_arg('reset', markers=['-reset'])
        ])

    def print_main_menu_view(self):
        output = _main_menu_template.format(cost_summary=self.subject.cost_summary)
        return self.app.fetch_component('standard_page_component').print(
            page_title='Cost Editor',
            page_content=output
        )

    def _validate_units(self, unit: str) -> str:
        try:
            unit = quantity.quantity_service.validate_qty_unit(unit)
        except quantity.exceptions.UnknownUnitError:
            raise pyconsoleapp.ResponseValidationError(
                'The unit is not recognised.')
        if quantity.quantity_service.units_are_volumes(unit) and not self.subject.density_is_defined:
            raise pyconsoleapp.ResponseValidationError('Density must be set before volumetric measurements can be used.')
        elif quantity.quantity_service.units_are_pieces(unit) and not self.subject.piece_mass_defined:
            raise pyconsoleapp.ResponseValidationError('Piece mass must be set before pieces can be used.')
        return unit

    def _validate_cost(self, cost_value: float) -> float:
        try:
            cost_value = cost.cost_service.validate_cost(cost_value)
        except cost.exceptions.CostValueError:
            raise pyconsoleapp.ResponseValidationError(
                'The cost must be a positive number')
        return cost_value

    def on_edit_cost(self, args) -> None:
        cost_per_single_unit = args['cost']/args['quantity']
        cost_per_g = quantity.quantity_service.convert_qty_unit(cost_per_single_unit, args['unit'], 'g',
            self.subject.readonly_bulk_data['g_per_ml'], self.subject.readonly_bulk_data['piece_mass_g'])
        self.subject.set_cost_per_g(cost_per_g)

    def on_save(self) -> None:
        self.save_func()

    def on_reset(self) -> None:
        self.subject.reset_cost_per_g()
        self.app.info_message = 'Cost data reset.'
