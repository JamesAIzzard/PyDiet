from typing import TYPE_CHECKING, cast

from pyconsoleapp import ConsoleAppComponent, styles

from pydiet import ingredients, persistence

if TYPE_CHECKING:
    from pydiet.ingredients.ingredient import Ingredient
    from pydiet.cost.cli_components.cost_editor_component import CostEditorComponent

_main_menu_template = '''
----------------|-------------
Save Changes    | -save
----------------|-------------
Edit Name       | -name [name]
Edit Cost       | -cost
Edit Flags      | -flag
Edit Bulk       | -bulk
Edit Nutrients  | -nuts
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
        self.subject: 'Ingredient'

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
        except (persistence.exceptions.UniqueValueDuplicatedError):
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
            ced = cast('CostEditorComponent', self.app.fetch_component('cost_editor_component'))
            ced.subject = self.subject
            ced.save_func = self.on_save
            self.app.goto('home.ingredients.edit.cost')
