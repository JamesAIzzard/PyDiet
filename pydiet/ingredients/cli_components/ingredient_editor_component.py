from typing import TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent

from pydiet import ingredients, nutrients, flags, quantity, cost

if TYPE_CHECKING:
    from pydiet.ingredients.ingredient import Ingredient

_main_menu_template = '''

Status: {status_summary}

Save Changes    | -save, -s
---------------------------------------------------
Ingredient Name:    {name} | -name, -n [name]
Edit Cost:          {cost} | -cost, -c
---------------------------------------------------
Weight/Density      | -weight, -w
{bulk_summary}
---------------------------------------------------
Flags:              | -flags, -f
{flags_summary}
---------------------------------------------------
Nutrients:          | -nutrients, -nut
{nutrients_summary}
'''


class IngredientEditorComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self.subject: 'Ingredient'

        self.configure_printer(self.print_main_menu_view)

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

    def _check_name_defined(self) -> bool:
        if not self._ies.ingredient.name:
            self.app.error_message = 'Ingredient name must be set first.'
            return False
        else:
            return True

    def on_save(self) -> None:
        # If the ingredient is named;
        if self._check_name_defined():
            # Save it;
            self._ies.save_changes(redirect_to='home.ingredients.edit')
        # If it is unamed;
        else:
            # Tell the user it needs to be named;
            self.app.error_message = 'Cannot save an un-named ingredient.'

    def on_edit_name(self):
        self.app.goto('home.ingredients.edit.name')

    def on_edit_cost(self):
        if self._check_name_defined():
            self.app.goto('home.ingredients.edit.cost_qty')

    def on_configure_liquid_measurements(self):
        if self._check_name_defined():
            self.app.goto('home.ingredients.edit.density_volume')

    def on_edit_flags(self):
        if self._check_name_defined():
            if self._ies.ingredient.all_flags_undefined:
                self.app.goto('home.ingredients.edit.flags.ask_cycle_flags')
            else:
                self.app.goto('home.ingredients.edit.flags')

    def on_edit_nutrients(self) -> None:
        if self._check_name_defined():
            self.app.goto('home.ingredients.edit.nutrients')
