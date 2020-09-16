from typing import Optional, TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent, builtin_validators, styles, ResponseValidationError

from pydiet import cost, quantity
import pydiet

if TYPE_CHECKING:
    from pydiet.cost.supports_cost import SupportsCostSetting

_main_menu_template = '''
----------------|------------------------------------------
OK              | -ok
Cancel          | -cancel
Zero Cost       | -reset
----------------|------------------------------------------
Set Cost        | -cost [cost] -per [quantity] -unit [unit]
----------------|------------------------------------------
Example         | -cost 2.50 -per 1.6 -unit kg
----------------|------------------------------------------

{cost_summary}

'''


class CostEditorComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self.subject: 'SupportsCostSetting'
        self._unchanged_cost_per_g: Optional[float]
        self._return_to_route: str

        self.configure_printer(self.print_main_menu_view)

        self.configure_responder(self.on_edit_cost, args=[
            self.configure_std_primary_arg(
                'cost', markers=['-cost'], validators=[self._validate_cost]),
            self.configure_std_primary_arg('per', markers=[
                '-per'], validators=[builtin_validators.validate_positive_nonzero_number]),
            self.configure_std_primary_arg('unit', markers=[
                '-unit'], validators=[self._validate_units])
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

    def print_main_menu_view(self):
        output = _main_menu_template.format(
            cost_summary=styles.fore(self.subject.cost_summary, 'blue'))
        return self.app.fetch_component('standard_page_component').print(
            page_title='Cost Editor',
            page_content=output
        )

    def _validate_units(self, unit: str) -> str:
        return quantity.cli_components.validators.validate_unit(self.subject, unit)

    def _validate_cost(self, cost_value: float) -> float:
        try:
            cost_value = cost.cost_service.validate_cost(cost_value)
        except cost.exceptions.CostValueError:
            raise ResponseValidationError(
                'The cost must be a positive number')
        return cost_value

    def on_edit_cost(self, args) -> None:
        self.subject.set_cost(args['cost'], args['per'], args['unit'])

    def on_ok(self, args) -> None:
        self.app.goto(self._return_to_route)

    def on_cancel(self, args) -> None:
        self.subject._set_cost_per_g(self._unchanged_cost_per_g)
        self.app.goto(self._return_to_route)

    def on_reset(self) -> None:
        self.subject.reset_cost()
        self.app.info_message = 'Cost data reset.'
