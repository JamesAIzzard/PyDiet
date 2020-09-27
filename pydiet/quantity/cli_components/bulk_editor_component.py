from typing import Optional, TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent, styles, builtin_validators
from pydiet import quantity

if TYPE_CHECKING:
    from pydiet.quantity.supports_bulk import SupportsBulkSetting, BulkData

_main_editor_template = '''
----------------|-----------------------------------
OK              | -ok
Cancel          | -cancel
Zero Bulk       | -reset
----------------|-----------------------------------
Set Pref Unit   | -unit [preferred unit]
Set Ref Qty     | -qty  [reference quantity]
Set Density     | -density 
Set Piece Mass  | -piece
----------------|-----------------------------------

{bulk_summary}

'''

_density_editor_template = '''
----------------|-----------------------------------
OK              | -ok
Cancel          | -cancel
Zero Density    | -reset
----------------|-----------------------------------
Set Density     | -mass  [mass]
                | -munit [mass unit]
                | -vol   [volume]
                | -vunit [volume unit]
----------------|-----------------------------------

Density: {density_summary}

'''

_piece_mass_editor_template = '''
----------------|----------------------------------
OK              | -ok
Cancel          | -cancel
Zero Piece Mass | -reset
----------------|----------------------------------
Set Piece Mass  | -num   [num pieces]
                | -mass  [mass]
                | -munit [mass unit]
----------------|----------------------------------

Piece Mass: {piece_mass_summary}

'''


class BulkEditorComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self.subject: 'SupportsBulkSetting'
        self._unchanged_bulk_data: 'BulkData'
        self._unchanged_g_per_ml: Optional[float]
        self._unchanged_piece_mass_g: Optional[float]
        self._return_to_route: str

        self.configure_states(['main', 'density', 'piece'])

        # Configure main mode;
        self.configure_printer(self._print_main_editor, ['main'])
        self.configure_responder(self._on_return_to_route, states=['main'], args=[
            self.configure_valueless_primary_arg('ok', markers=['-ok'])
        ])
        self.configure_responder(self._on_cancel_and_return_to_route, states=['main'], args=[
            self.configure_valueless_primary_arg('cancel', markers=['-cancel'])
        ])
        self.configure_responder(self._on_set_pref_unit, states=['main'], args=[
            self.configure_std_primary_arg(
                'pref_unit', markers=['-unit'], validators=[self._validate_configured_unit])
        ])
        self.configure_responder(self._on_set_ref_quantity, states=['main'], args=[
            self.configure_std_primary_arg('ref_qty', markers=['-qty'], validators=[
                builtin_validators.validate_positive_nonzero_number
            ])
        ])
        self.configure_responder(self._on_reset_bulk, states=['main'], args=[
            self.configure_valueless_primary_arg('reset', markers=['-reset'])
        ])
        self.configure_responder(self._on_goto_density_editor, states=['main'], args=[
            self.configure_valueless_primary_arg(
                'density', markers=['-density'])
        ])
        self.configure_responder(self._on_goto_piece_editor, states=['main'], args=[
            self.configure_valueless_primary_arg(
                'piece', markers=['-piece'])
        ])

        # Configure density mode;
        self.configure_printer(self._print_density_editor, ['density'])
        self.configure_responder(self.make_state_changer('main'), states=['density'], args=[
            self.configure_valueless_primary_arg('ok', markers=['-ok'])
        ])
        self.configure_responder(self._on_reset_density, states=['density'], args=[
            self.configure_valueless_primary_arg('reset', markers=['-reset'])
        ])
        self.configure_responder(self._on_cancel_density_and_return_to_main, states=['density'], args=[
            self.configure_valueless_primary_arg('cancel', markers=['-cancel'])
        ])
        self.configure_responder(self._on_set_density, states=['density'], args=[
            self.configure_std_primary_arg('mass', markers=[
                '-mass'], validators=[builtin_validators.validate_positive_nonzero_number]),
            self.configure_std_primary_arg(
                'munit', markers=['-munit'], validators=[quantity.cli_components.validators.validate_mass_unit]),
            self.configure_std_primary_arg('vol', markers=[
                '-vol'], validators=[builtin_validators.validate_positive_nonzero_number]),
            self.configure_std_primary_arg(
                'vunit', markers=['-vunit'], validators=[quantity.cli_components.validators.validate_vol_unit])
        ])

        # Configure piece mass mode;
        self.configure_printer(self._print_piece_mass_editor, ['piece'])
        self.configure_responder(self.make_state_changer('main'), states=['piece'], args=[
            self.configure_valueless_primary_arg('ok', markers=['-ok'])
        ])
        self.configure_responder(self._on_cancel_piece_and_return_to_main, states=['piece'], args=[
            self.configure_valueless_primary_arg('cancel', markers=['-cancel'])
        ])
        self.configure_responder(self._on_reset_piece, states=['piece'], args=[
            self.configure_valueless_primary_arg('reset', markers=['-reset'])
        ])
        self.configure_responder(self._on_set_piece_mass, states=['piece'], args=[
            self.configure_std_primary_arg('num', markers=['-num'],
                                           validators=[builtin_validators.validate_positive_nonzero_number]),
            self.configure_std_primary_arg('mass', markers=['-mass'],
                                           validators=[builtin_validators.validate_positive_nonzero_number]),
            self.configure_std_primary_arg('munit', markers=['-munit'],
                                           validators=[quantity.cli_components.validators.validate_mass_unit])
        ])

        # Shared methods;

    def _validate_configured_unit(self, unit):
        return quantity.cli_components.validators.validate_configured_unit(self.subject, unit)

    # Main editor methods;
    def _print_main_editor(self):
        output = _main_editor_template.format(
            bulk_summary=styles.fore(self.subject.bulk_summary, 'blue'))
        return self.app.fetch_component('standard_page_component').print(
            page_title='Bulk Editor',
            page_content=output
        )

    def _on_set_pref_unit(self, args):
        self.subject.set_pref_unit(args['pref_unit'])

    def _on_set_ref_quantity(self, args):
        self.subject.set_ref_qty(args['ref_qty'])

    def _on_return_to_route(self):
        self.app.goto(self._return_to_route)

    def _on_cancel_and_return_to_route(self):
        self.subject.set_bulk_data(self._unchanged_bulk_data)
        self.app.goto(self._return_to_route)

    def _on_reset_bulk(self):
        self.subject.reset_bulk()

    def _on_goto_density_editor(self):
        if self.subject.density_is_defined:
            self._unchanged_g_per_ml = self.subject.g_per_ml
        else:
            self._unchanged_g_per_ml = None
        self.current_state = 'density'

    def _on_goto_piece_editor(self):
        if self.subject.piece_mass_defined:
            self._unchanged_piece_mass_g = self.subject.piece_mass_g
        else:
            self._unchanged_piece_mass_g = None
        self._unchanged_piece_mass_g = self.subject.piece_mass_g
        self.current_state = 'piece'

    # Density editor methods;
    def _print_density_editor(self):
        output = _density_editor_template.format(
            density_summary=styles.fore(self.subject.density_summary, 'blue'))
        return self.app.fetch_component('standard_page_component').print(
            page_title='Density Editor',
            page_content=output
        )

    def _on_cancel_density_and_return_to_main(self):
        self.subject.set_g_per_ml(self._unchanged_g_per_ml)

    def _on_reset_density(self):
        self.subject.reset_density()

    def _on_set_density(self, args):
        self.subject.set_density(
            args['mass'], args['munit'], args['vol'], args['vunit'])

    # Piece mass editor methods;
    def _print_piece_mass_editor(self):
        output = _piece_mass_editor_template.format(
            piece_mass_summary=styles.fore(self.subject.piece_mass_summary, 'blue'))
        return self.app.fetch_component('standard_page_component').print(
            page_title='Piece Mass Editor',
            page_content=output
        )

    def _on_cancel_piece_and_return_to_main(self):
        self.subject.set_piece_mass_g(self._unchanged_piece_mass_g)

    def _on_reset_piece(self):
        self.subject.reset_piece_mass()

    def _on_set_piece_mass(self, args):
        self.subject.set_piece_mass(args['num'], args['mass'], args['munit'])
