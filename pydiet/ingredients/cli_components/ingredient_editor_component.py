from typing import TYPE_CHECKING

import pydiet
from pyconsoleapp import styles, PrimaryArg, builtin_validators
from pydiet import ingredients, persistence, flags, nutrients, quantity

if TYPE_CHECKING:
    from pydiet.ingredients.ingredient import Ingredient

_menu_screen_template = '''OK & Save   | -ok
Cancel      | -cancel

Ingredient Status: {status_summary}

Name | -name [name] -> {name}

Cost | -cost [cost] -per [qty] -> {cost}

Bulk (Weight & Density) | -bulk ->
{bulk_summary}

Flags | -flags ->
{flags_summary}

Nutrients | -nutr ->      
{nutrients_summary}
'''


class IngredientEditorComponent(pydiet.cli_components.BaseEditorComponent):
    def __init__(self, app):
        super().__init__(app)

        self.configure_state('menu', self._print_menu_screen, responders=[
            self.configure_responder(self._on_ok_and_save, args=[
                PrimaryArg('save', has_value=False, markers=['-ok'])]),
            self.configure_responder(self._on_edit_name, args=[
                PrimaryArg('name', has_value=True, markers=['-name'])]),
            self.configure_responder(self._on_edit_cost, args=[
                PrimaryArg('cost', has_value=True, markers=['-cost'], validators=[
                    builtin_validators.validate_positive_nonzero_number]),
                PrimaryArg('per', has_value=True, markers=['-per'], validators=[
                    self._validate_cost_per_input])]),
            self.configure_responder(self._on_edit_flags, args=[
                PrimaryArg('flags', has_value=False, markers=['-flags'])]),
            self.configure_responder(self._on_edit_bulk, args=[
                PrimaryArg('bulk', has_value=False, markers=['-bulk'])]),
            self.configure_responder(self._on_edit_nutrients, args=[
                PrimaryArg('nutr', has_value=False, markers=['-nutr'])])
        ])

    def _print_menu_screen(self):
        output = _menu_screen_template.format(
            status_summary=styles.fore(self._subject.completion_status_summary, 'blue'),
            name=styles.fore(str(self._subject.name_summary), 'blue'),
            cost=styles.fore(self._subject.cost_summary, 'blue'),
            bulk_summary=styles.fore(self._subject.bulk_summary, 'blue'),
            flags_summary=styles.fore(self._subject.flags_summary, 'blue'),
            nutrients_summary=styles.fore(self._subject.nutrients_summary, 'blue'))
        return self.app.fetch_component('standard_page_component').print(
            page_title='Ingredient Editor',
            page_content=output
        )

    def _check_if_name_defined(self) -> bool:
        if not self._subject.name_is_defined:
            self.app.error_message = 'Ingredient name must be set first.'
            return False
        else:
            return True

    def _validate_cost_per_input(self, value):
        qty, unit = builtin_validators.validate_number_and_str(value)
        qty = builtin_validators.validate_positive_nonzero_number(qty)
        unit = quantity.cli_components.validators.validate_configured_unit(self._subject, unit)
        return {'qty': qty, 'unit': unit}

    def _on_edit_name(self, args):
        if not persistence.persistence_service.check_unique_val_avail(
                ingredients.ingredient.Ingredient,
                self._subject.datafile_name,
                args['name']):
            self.app.error_message = 'There is already an ingredient called {}.'.format(
                args['name'])
        self._subject.set_name(args['name'])

    def _on_edit_cost(self, args):
        if self._check_if_name_defined():
            self._subject.set_cost(args['cost'], args['per']['qty'], args['per']['unit'])

    def _on_edit_flags(self):
        if self._check_if_name_defined():
            fed = self.app.get_component(flags.cli_components.flag_editor_component.FlagEditorComponent)
            fed.configure(subject=self._subject, return_to_route=self.app.route,
                          backup_flag_data=self._subject.flags_data_copy)
            self.app.goto('home.ingredients.edit.flags')

    def _on_edit_bulk(self):
        if self._check_if_name_defined():
            bed = self.app.get_component(quantity.cli_components.bulk_editor_component.BulkEditorComponent)
            bed.configure(self._subject, self._subject.bulk_data_copy)
            self.app.goto('home.ingredients.edit.bulk')

    def _on_edit_nutrients(self) -> None:
        if self._check_if_name_defined():
            ned = self.app.get_component(
                nutrients.cli_components.nutrient_content_editor_component.NutrientContentEditorComponent)
            ned.configure(subject=self._subject, return_to_route=self.app.route,
                          backup_nutrients_data=self._subject.nutrients_data_copy)
            ned.change_state('main')
            self.app.goto('home.ingredients.edit.nutrients')

    def configure(self, subject: 'Ingredient') -> None:
        guard_exit_route = 'home.ingredients.edit'
        guard = self.app.get_component(ingredients.cli_components.IngredientSaveCheckGuardComponent)
        guard.configure(subject=subject)
        super()._configure(subject, guard_exit_route=guard_exit_route, guard=guard,
                           return_to_route='home.ingredients')
