from typing import Optional, TYPE_CHECKING, cast

from pyconsoleapp import ConsoleAppComponent

from pydiet import ingredients, nutrients, flags, quantity, cost, persistence

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
        self.subject_datafile_name: Optional[str] = None

        self.configure_printer(self.print_main_menu_view)

        self.configure_responder(self.on_save, args=[
            self.configure_valueless_primary_arg('save', markers=['-save'])
        ])

        self.configure_responder(self.on_edit_name, args=[
            self.configure_std_primary_arg('name', markers=['-name'])
        ])

    def print_main_menu_view(self):
        output = _main_menu_template.format(
            status_summary=self.subject.status_summary,
            name=self.subject.name,
            cost=self.subject.cost_summary,
            bulk_summary=self.subject.bulk_summary,
            flags_summary=self.subject.flags_summary,
            nutrients_summary=self.subject.nutrients_summary
        )
        return self.app.fetch_component('standard_page_component').print(
            page_title='Ingredient Editor',
            page_content=output
        )

    def _check_if_name_defined(self) -> bool:
        if not self.subject.name:
            self.app.error_message = 'Ingredient name must be set first.'
            return False
        else:
            return True

    def on_save(self) -> None:
        if not self._check_if_name_defined():
            return
        persistence.persistence_service.save(self.subject)

    def on_edit_name(self, args):
        if ingredients.ingredient_service.check_if_name_taken(args['name'],
                                                              self.subject_datafile_name):
            self.app.error_message = 'There is already an ingredient called {}.'.format(
                args['name'])
            return
        self.subject.name = args['name']

    # def on_edit_cost(self):
    #     if self._check_name_defined():
    #         self.app.goto('home.ingredients.edit.cost_qty')

    # def on_configure_liquid_measurements(self):
    #     if self._check_name_defined():
    #         self.app.goto('home.ingredients.edit.density_volume')

    # def on_edit_flags(self):
    #     if self._check_name_defined():
    #         if self._ies.ingredient.all_flags_undefined:
    #             self.app.goto('home.ingredients.edit.flags.ask_cycle_flags')
    #         else:
    #             self.app.goto('home.ingredients.edit.flags')

    # def on_edit_nutrients(self) -> None:
    #     if self._check_name_defined():
    #         self.app.goto('home.ingredients.edit.nutrients')
