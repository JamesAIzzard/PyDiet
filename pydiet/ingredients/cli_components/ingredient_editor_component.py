from typing import Optional, TYPE_CHECKING, cast

from pyconsoleapp import ConsoleAppComponent, styles
from pydiet import ingredients, persistence, cost, flags, nutrients

if TYPE_CHECKING:
    from pydiet.ingredients.ingredient import Ingredient

_main_menu_template = '''
----------------|-------------
Save Changes    | -save
----------------|-------------
Edit Name       | -name [name]
Edit Cost       | -cost
Edit Flags      | -flag
Edit Bulk       | -bulk
Edit Nutrients  | -nutr
----------------|-------------

Ingredient Status: {status_summary}

Name: {name}
Cost: {cost}

Bulk (Weight & Density):
{bulk_summary}

Flags:
{flags_summary}

Nutrients:
{nutrients_summary}
'''


class IngredientEditorComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self.subject: Optional['Ingredient'] = None

        self.configure_printer(self.print_main_menu_view)

        self.configure_responder(self.on_save, args=[
            self.configure_valueless_primary_arg('save', markers=['-save'])
        ])

        self.configure_responder(self.on_edit_name, args=[
            self.configure_std_primary_arg('name', markers=['-name'])
        ])

        self.configure_responder(self.on_edit_cost, args=[
            self.configure_valueless_primary_arg('cost', markers=['-cost'])
        ])

        self.configure_responder(self.on_edit_flags, args=[
            self.configure_valueless_primary_arg('flag', markers=['-flag'])
        ])

        self.configure_responder(self.on_edit_nutrients, args=[
            self.configure_valueless_primary_arg('nutr', markers=['-nutr'])
        ])

        self.configure_responder(self.on_edit_bulk, args=[
            self.configure_valueless_primary_arg('bulk', markers=['-bulk'])
        ])

    def print_main_menu_view(self):
        output = _main_menu_template.format(
            status_summary=styles.fore(self.subject.status_summary, 'blue'),
            name=styles.fore(str(self.subject.name_summary), 'blue'),
            cost=styles.fore(self.subject.cost_summary, 'blue'),
            bulk_summary=styles.fore(self.subject.bulk_summary, 'blue'),
            flags_summary=styles.fore(self.subject.flags_summary, 'blue'),
            nutrients_summary=styles.fore(self.subject.nutrients_summary, 'blue'))
        return self.app.fetch_component('standard_page_component').print(
            page_title='Ingredient Editor',
            page_content=output
        )

    def _check_if_name_defined(self) -> bool:
        if not self.subject.name_is_defined:
            self.app.error_message = 'Ingredient name must be set first.'
            return False
        else:
            return True

    def on_save(self) -> None:
        if not self._check_if_name_defined():
            return
        try:
            persistence.persistence_service.save(self.subject)
            self.app.info_message = 'Ingredient saved.'
        except persistence.exceptions.UniqueValueDuplicatedError:
            self.app.error_message = 'There is already an ingredient called {}.'.format(
                self.subject.name
            )

    def on_edit_name(self, args):
        if not persistence.persistence_service.check_unique_val_avail(
                ingredients.ingredient.Ingredient,
                self.subject.datafile_name,
                args['name']):
            self.app.error_message = 'There is already an ingredient called {}.'.format(
                args['name'])
        self.subject.set_name(args['name'])

    def on_edit_cost(self):
        if self._check_if_name_defined():
            ced = self.app.get_component(cost.cli_components.cost_editor_component.CostEditorComponent)
            ced.configure(subject=self.subject, backup_cost_per_g=self.subject.cost_per_g, return_to=self.app.route)
            self.app.goto('home.ingredients.edit.cost')

    def on_edit_flags(self):
        if self._check_if_name_defined():
            fed = self.app.get_component(flags.cli_components.flag_editor_component.FlagEditorComponent)
            fed.configure(subject=self.subject, return_to_route=self.app.route,
                          backup_flag_data=self.subject.flags_data_copy)
            self.app.goto('home.ingredients.edit.flags')

    def on_edit_bulk(self):
        if self._check_if_name_defined():
            bed = cast('BulkEditorComponent', self.app.fetch_component('bulk_editor_component'))
            bed.subject = self.subject
            bed._unchanged_bulk_data = self.subject.bulk_data_copy
            bed._return_to_route = self.app.route
            self.app.goto('home.ingredients.edit.bulk')

    def on_edit_nutrients(self) -> None:
        if self._check_if_name_defined():
            ned = self.app.get_component(
                nutrients.cli_components.nutrient_content_editor_component.NutrientContentEditorComponent)
            ned.configure(subject=self.subject, return_to_route=self.app.route,
                          backup_nutrients_data=self.subject.nutrients_data_copy)
            ned.change_state('main')
            self.app.goto('home.ingredients.edit.nutrients')
