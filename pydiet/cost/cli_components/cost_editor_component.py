from typing import Optional, TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent, builtin_validators, styles
from pydiet import cost, quantity

if TYPE_CHECKING:
    from pydiet.cost.supports_cost import SupportsCostSetting

_main_editor_template = '''
----------------|-------------------------------------------
OK              | -ok
Cancel          | -cancel
Zero Cost       | -reset
----------------|-------------------------------------------
Set Cost        | -cost [cost] -per [quantity] -unit [unit]
----------------|-------------------------------------------
Example         | -cost 2.50 -per 1.6 -unit kg
----------------|-------------------------------------------

Cost Summary: {cost_summary}

'''


class CostEditorComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self.subject: Optional['SupportsCostSetting'] = None
        self._backup_cost_per_g: Optional[float] = None
        self._return_to_route: Optional[str] = None

        # Configure main mode;
        self.configure_printer(self.print_main_editor)
        self.configure_responder(self.on_edit_cost, args=[
            self.configure_std_primary_arg(
                'cost', markers=['-cost'], validators=[cost.cli_components.validators.validate_cost]),
            self.configure_std_primary_arg('per', markers=[
                '-per'], validators=[builtin_validators.validate_positive_nonzero_number]),
            self.configure_std_primary_arg('unit', markers=[
                '-unit'], validators=[self._validate_configured_unit])
        ])
        self.configure_responder(self.on_reset, args=[
            self.configure_valueless_primary_arg('reset', markers=['-reset'])
        ])
        self.configure_responder(self.on_ok, args=[
            self.configure_valueless_primary_arg('ok', markers=['-ok'])
        ])
        self.configure_responder(self.on_cancel, args=[
            self.configure_valueless_primary_arg('cancel', markers=['-cancel'])
        ])

    def configure(self, subject: 'SupportsCostSetting', backup_cost_per_g: float, return_to: str):
        self.subject = subject
        self._backup_cost_per_g = backup_cost_per_g,
        self._return_to_route = return_to

    def print_main_editor(self):
        output = _main_editor_template.format(
            cost_summary=styles.fore(self.subject.cost_summary, 'blue'))
        return self.app.fetch_component('standard_page_component').print(
            page_title='Cost Editor',
            page_content=output
        )

    def on_edit_cost(self, args) -> None:
        self.subject.set_cost(args['cost'], args['per'], args['unit'])

    def on_ok(self, args) -> None:
        self.app.goto(self._return_to_route)

    def on_cancel(self, args) -> None:
        self.subject.set_cost_per_g(self._unchanged_cost_per_g)
        self.app.goto(self._return_to_route)

    def on_reset(self) -> None:
        self.subject.reset_cost()
        self.app.info_message = 'Cost data reset.'

    def _validate_configured_unit(self, unit: str) -> str:
        return quantity.cli_components.validators.validate_configured_unit(self.subject, unit)
