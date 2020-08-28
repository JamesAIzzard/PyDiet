from pydiet.ingredients import ingredient
from typing import TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent

from pydiet import ingredients, nutrients, flags, quantity, cost

if TYPE_CHECKING:
    from pydiet.ingredients.ingredient import Ingredient

_main_menu_template = '''

Status: {status}

Save Changes    | -save, -s
---------------------------------------------------
Ingredient Name:    {name:>10} | -name, -n [name]
Edit Cost:          {cost:>10} | -cost, -c
Configure Liquid:   {density_status:>} | -liquid, -l
---------------------------------------------------
Flags:              | -flags, -f
{flag_summary}
---------------------------------------------------
Nutrients:          | -nutrients, -nut
{nutrient_summary}
'''


class IngredientEditorComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self.subject: 'Ingredient'

        self.configure_printer(self.print_main_menu_view)

    def print_main_menu_view(self):
        # Build the nutrient summary;
        nutrient_summary = ''  # string for nutrient display
        # Start with the primary nutrients;
        primary_nutrients = self.subject.primary_nutrient_amounts
        for pnn in primary_nutrients.keys():
            nutrient_summary = nutrient_summary + \
                '- {}\n'.format(nutrients.nutrients_service.print_nutrient_amount_summary(
                    primary_nutrients[pnn]))
        # Now do any defined secondary nutrients;
        defined_secondary_nutrients = self.subject.defined_secondary_nutrient_amounts
        for dsnn in defined_secondary_nutrients:
            nutrient_summary = nutrient_summary + \
                '- {}\n'.format(nutrients.nutrients_service.print_nutrient_amount_summary(
                    defined_secondary_nutrients[dsnn]))

        # Build the flag summary;
        flag_summary = ''
        for flag_name in self.subject.flags.keys():
            flag_summary = flag_summary + '- {}\n'.format(flags.flags_service.print_flag_summary(
                flag_name=flag_name,
                flag_value=self.subject.get_flag(flag_name)
            ))

        # Assemble the template
        output = _main_menu_template.format(
            status=ingredients.ingredient_service.summarise_status(self.subject),
            name=self.subject.name,
            cost=cost.cost_service.print_cost_summary(self.subject),
            density_status=quantity.quantity_service.print_density_summary(self.subject),
            flags=flag_summary,
            nutrients=nutrient_summary
        )
        output = self.app.fetch_component(
            'standard_page_component').call_print(output)
        return output

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
