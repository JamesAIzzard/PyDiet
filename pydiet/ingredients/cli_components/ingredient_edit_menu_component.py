from pyconsoleapp import ConsoleAppComponent

from pydiet import repository_service as rps
from pydiet.ingredients import ingredient_service as igs
from pydiet.ingredients import ingredient_edit_service as ies

_TEMPLATE = '''Ingredient Editor:
------------------

Status: {status}

(s) -- Save Changes

(1) -- Edit Name: {name}

(2) -- Edit Cost: {cost}

(3) -- Configure Liquid Measurements: {density_status}

(4) -- Edit Flags:
{flags}
(5) -- Edit Nutrients:
{nutrients}
'''


class IngredientEditMenuComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self._ies = ies.IngredientEditService()
        self.set_option_response('1', self.on_edit_name)
        self.set_option_response('2', self.on_edit_cost)
        self.set_option_response('3', self.on_configure_liquid_measurements)
        self.set_option_response('4', self.on_edit_flags)
        self.set_option_response('5', self.on_edit_nutrients)
        self.set_option_response('s', self.on_save)

    def run(self):
        # If we shouldn't be here;
        if not self._ies.ingredient or not self._ies.mode == 'edit':
            # Go back another level;
            self.app.goto('home.ingredients')

    def print(self):
        # Raise exception if ingredient has not been loaded;
        if not self._ies.ingredient:
            raise AttributeError
        # Build the nutrient summary;
        n = ''  # string for nutrient display
        # Start with the primary nutrients;
        primary_nutrients = self._ies.ingredient.primary_nutrients
        for pnn in primary_nutrients.keys():
            n = n + '- {}\n'.format(igs.
                                    summarise_nutrient_amount(primary_nutrients[pnn]))
        # Now do any defined secondary nutrients;
        defined_secondary_nutrients = self._ies.ingredient.defined_secondary_nutrients
        for dsnn in defined_secondary_nutrients:
            n = n + '- {}\n'.format(igs.
                                    summarise_nutrient_amount(defined_secondary_nutrients[dsnn]))
        # Build the flag summary;
        f = ''
        for flag_name in self._ies.ingredient.all_flag_data.keys():
            f = f + '- {}\n'.format(igs.summarise_flag(
                self._ies.ingredient,
                flag_name
            ))
        # Assemble the template
        output = _TEMPLATE.format(
            status=igs.summarise_status(self._ies.ingredient),
            name=igs.summarise_name(self._ies.ingredient),
            cost=igs.summarise_cost(self._ies.ingredient),
            density_status=igs.summarise_density(self._ies.ingredient),
            flags=f,
            nutrients=n
        )
        output = self.app.fetch_component('standard_page_component').call_print(output)
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
