from typing import Optional, Dict, TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent, PrimaryArg, builtin_validators, StandardPageComponent
from pydiet import quantity

if TYPE_CHECKING:
    from pydiet.quantity.supports_bulk import SupportsBulkSetting, BulkData
    from pydiet.quantity.cli_components.validators import QtyAndUnit

_main_screen_template = '''
OK                  | -ok
Cancel              | -cancel

Set Ref Amount      | -ref [ref_amount] -> {ref_amount_summary}

Clear Density       | -clrd
Set Density         | -vol [volume] -weighs [weight_of_volume] ->
{density_summary}

Clear Piece Mass    | -clrp
Set Piece Mass      | -pieces [num_pieces] -weighs [weight_of_pieces] ->
{pc_mass_summary}
'''


class BulkEditorComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self._subject: Optional['SupportsBulkSetting'] = None
        self._backup_bulk_data: Optional['BulkData'] = None

        self.configure_state('main', self._print_main_screen, responders=[
            self.configure_responder(self._on_ok, args=[
                PrimaryArg('ok', has_value=False, markers=['-ok'])]),
            self.configure_responder(self._on_cancel, args=[
                PrimaryArg('cancel', has_value=False, markers=['-cancel'])]),
            self.configure_responder(self._on_set_ref_amount, args=[
                PrimaryArg('ref_amount', has_value=True, markers=['-ref'], validators=[self._validate_ref_amount])]),
            self.configure_responder(self._on_clear_density, args=[
                PrimaryArg('clear_density', has_value=False, markers=['-clrd'])]),
            self.configure_responder(self._on_set_density, args=[
                PrimaryArg('volume', has_value=True, markers=['-vol'],
                           validators=[quantity.cli_components.validators.validate_volume_qty_and_unit]),
                PrimaryArg('weight_of_volume', has_value=True, markers=['-weighs'],
                           validators=[quantity.cli_components.validators.validate_mass_qty_and_unit])]),
            self.configure_responder(self._on_clear_piece_mass, args=[
                PrimaryArg('clear_pc_mass', has_value=True, markers=['-clrp'])]),
            self.configure_responder(self._on_set_piece_mass, args=[
                PrimaryArg('num_pieces', has_value=True, markers=['-pieces'],
                           validators=[builtin_validators.validate_positive_nonzero_number]),
                PrimaryArg('weight_of_pieces', has_value=True, markers=['-weighs'],
                           validators=[quantity.cli_components.validators.validate_mass_qty_and_unit])
            ])
        ])

    def _print_main_screen(self) -> str:
        return self.app.get_component(StandardPageComponent).print_view(
            page_title='Bulk Editor',
            page_content=_main_screen_template.format(
                ref_amount_summary=self._subject.ref_amount_summary,
                density_summary=self._subject.density_summary,
                pc_mass_summary=self._subject.piece_mass_summary
            )
        )

    def _validate_ref_amount(self, value: str) -> Dict:
        ref_amount = builtin_validators.validate_number_and_str(value)
        qty = builtin_validators.validate_positive_nonzero_number(ref_amount[0])
        unit = quantity.cli_components.validators.validate_configured_unit(self._subject, ref_amount[1])
        return {'qty': qty, 'unit': unit}

    def _on_ok(self) -> None:
        self.app.goto('home.ingredients.edit')

    def _on_cancel(self) -> None:
        self._subject.set_bulk_data(self._backup_bulk_data)
        self.app.goto('home.ingredients.edit')

    def _on_set_ref_amount(self, args) -> None:
        self._subject.set_ref_qty(args['ref_amount']['qty'])
        self._subject.set_ref_unit(args['ref_amount']['unit'])

    def _on_clear_density(self) -> None:
        self._subject.reset_density()

    def _on_set_density(self, args: Dict[str, 'QtyAndUnit']) -> None:
        self._subject.set_density(args['weight_of_volume']['qty'],
                                  args['weight_of_volume']['unit'],
                                  args['volume']['qty'],
                                  args['volume']['unit'])

    def _on_clear_piece_mass(self) -> None:
        self._subject.reset_piece_mass()

    def _on_set_piece_mass(self, args) -> None:
        self._subject.set_piece_mass(args['num_pieces'],
                                     args['weight_of_pieces']['qty'],
                                     args['weight_of_pieces']['unit'])

    def configure(self, subject: 'SupportsBulkSetting', backup_data: 'BulkData') -> None:
        self._subject = subject
        self._backup_bulk_data = backup_data
