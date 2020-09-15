from typing import TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent, styles

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

        self.configure_printer(self.print_main_editor, ['main'])
        self.configure_printer(self.print_density_editor, ['density'])
        self.configure_printer(self.print_piece_mass_editor, ['piece'])

    def print_main_editor(self):
        output = _main_editor_template.format(
            bulk_summary=styles.fore(self.subject.bulk_summary, 'blue'))
        return self.app.fetch_component('standard_page_component').print(
            page_title='Bulk Editor',
            page_content=output
        )

    def print_density_editor(self):
        output = _density_editor_template.format(
            density_summary=styles.fore(self.subject.density_summary, 'blue'))
        return self.app.fetch_component('standard_page_component').print(
            page_title='Density Editor',
            page_content=output
        )

    def print_piece_mass_editor(self):
        output = _piece_mass_editor_template.format(
            piece_mass_summary=styles.fore(self.subject.piece_mass_summary, 'blue'))
        return self.app.fetch_component('standard_page_component').print(
            page_title='Piece Mass Editor',
            page_content=output
        )                   