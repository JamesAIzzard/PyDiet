from pinjector import inject
from pyconsoleapp import ConsoleAppComponent

from pydiet.cli.ingredients import ingredient_edit_service as ies
from pydiet.ingredients import ingredient_service as igs


_TEMPLATE = '''Nutrient Editor:
----------------

(s) -- Save Changes

Primary Nutrients (Required):
{primary_nutrients}

Other Nutrients (Optional):
{secondary_nutrients}

(n) -- Edit Other Nutrients
'''


class EditIngredientNutrientMenuComponent(ConsoleAppComponent):

    def __init__(self):
        super().__init__()
        self._ies = ies.IngredientEditService()
        self.set_option_response('n', self.on_edit_other)
        self.set_option_response('s', self.on_save_changes)

    def print(self):
        # First build the primary nutrient string;
        pn = ''  # primary nutrient string
        pnmap = self._ies.primary_nutrient_number_name_map
        for option_number in pnmap:
            na = self._ies.ingredient.get_nutrient_amount(pnmap[option_number])
            pn = pn + '({}) -- {}\n'.format(
                option_number,
                igs.summarise_nutrient_amount(na)
            )
        # Now build the secondary nutrient string;
        sn = ''  # secondary nutrient string;
        snmap = self._ies.defined_secondary_nutrient_number_name_map
        if len(snmap.keys()):
            for option_number in snmap:
                na = self._ies.ingredient.get_nutrient_amount(
                    snmap[option_number])
                sn = sn + '({}) -- {}\n'.format(
                    option_number,
                    igs.summarise_nutrient_amount(na)
                )
        else:
            sn = 'None defined.'
        output = _TEMPLATE.format(
            primary_nutrients=pn,
            secondary_nutrients=sn
        )
        output = self.app.fetch_component(
            'standard_page_component').print(output)
        return output

    def on_save_changes(self) -> None:
        self._ies.save_changes()

    def on_edit_other(self):
        self.app.goto('home.ingredients.edit.nutrients.search')

    def dynamic_response(self, response):
        # Try and parse the response as an int;
        try:
            response = int(response)
        except ValueError:
            return None
        # If the response is one of the numbered nutrients;
        number_map = self._ies.primary_nutrient_number_name_map
        number_map.update(self._ies.defined_secondary_nutrient_number_name_map)
        if response in number_map.keys():
            # Get the nutrient name;
            nutrient_name = self._ies.primary_nutrient_number_name_map[int(
                response)]
            # Load that nutrient as the current nutrient amount;
            self._ies.current_nutrient_amount = \
                self._ies.ingredient.get_nutrient_amount(nutrient_name)
            self.app.goto(
                'home.ingredients.edit.nutrients.nutrient_ingredient_qty')
