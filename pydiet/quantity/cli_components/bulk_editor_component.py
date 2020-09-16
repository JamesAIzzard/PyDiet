from typing import TYPE_CHECKING

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
Set Pref Unit   | -unit
Set Ref Qty     | -qty
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

{density_summary}

'''

_piece_mass_editor_template = '''
----------------|----------------------------------
OK              | -ok
Cancel          | -cancel
Zero Peice Mass | -reset
----------------|----------------------------------
Set Density     | -mass  [mass]
                | -munit [mass unit]
                | -vol   [volume]
                | -vunit [volume unit]
----------------|----------------------------------

{piece_mass_summary}

'''

class BulkEditorComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self.subject: 'SupportsBulkSetting'
        self._unchanged_bulk_data: 'BulkData'
        self._return_to_route: str

        self.configure_states(['main', 'density', 'piece'])

        self.configure_printer(self._print_main_editor, ['main'])
        self.configure_responder(self._on_return_to_route, states=['main'], args=[
            self.configure_valueless_primary_arg('ok', markers=['-ok'])
        ])
        self.configure_responder(self._on_set_pref_unit, states=['main'], args=[
            self.configure_std_primary_arg('pref_unit', markers=['-unit'], validators=[self._validate_unit])
        ])
        self.configure_responder(self._on_set_ref_quantity, states=['main'], args=[
            self.configure_std_primary_arg('ref_qty', markers=['-qty'], validators=[
                builtin_validators.validate_positive_nonzero_number
            ])
        ])
        self.configure_responder(self.make_state_changer('density'), states=['main'], args=[
            self.configure_valueless_primary_arg('density', markers=['-density'])
        ])
        self.configure_responder(self.make_state_changer('piece'), states=['main'], args=[
            self.configure_valueless_primary_arg('piece', markers=['-piece'])
        ])           

        self.configure_printer(self._print_density_editor, ['density'])
        self.configure_printer(self._print_piece_mass_editor, ['piece'])        

    def _print_main_editor(self):
        output = _main_editor_template.format(
            bulk_summary=styles.fore(self.subject.bulk_summary, 'blue'))
        return self.app.fetch_component('standard_page_component').print(
            page_title='Bulk Editor',
            page_content=output
        )

    def _validate_unit(self, unit):
        return quantity.cli_components.validators.validate_unit(self.subject, unit)

    def _on_set_pref_unit(self, args):
        self.subject.set_pref_unit(args['pref_unit'])

    def _on_set_ref_quantity(self, args):
        self.subject.set_ref_qty(args['ref_qty'])

    def _on_return_to_route(self):
        self.app.goto(self._return_to_route)

    def _on_cancel_and_return_to_route(self):
        self.subject.set_bulk_data(self._unchanged_bulk_data)
        self.app.goto(self._return_to_route)


    def _print_density_editor(self):
        output = _density_editor_template.format(
            density_summary=styles.fore(self.subject.density_summary, 'blue'))
        return self.app.fetch_component('standard_page_component').print(
            page_title='Density Editor',
            page_content=output
        )

    def _print_piece_mass_editor(self):
        output = _piece_mass_editor_template.format(
            piece_mass_summary=styles.fore(self.subject.piece_mass_summary, 'blue'))
        return self.app.fetch_component('standard_page_component').print(
            page_title='Piece Mass Editor',
            page_content=output
        )
