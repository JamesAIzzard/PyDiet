from typing import TYPE_CHECKING, Dict, Union

from pinjector import inject

from pydiet.ingredients.exceptions import (
    NutrientQtyExceedsIngredientQtyError,
    ConstituentsExceedGroupError,
    NutrientAmountUndefinedError
)

if TYPE_CHECKING:
    from pydiet.ingredients.ingredient import Ingredient
    from pydiet.shared import utility_service
    from pydiet.shared import configs

class NutrientAmount():
    def __init__(
        self,
        name: str,
        parent_ingredient: 'Ingredient'
    ):
        self.name = name
        self._us:'utility_service' = inject('pydiet.utility_service')
        self._cf:'configs' = inject('pydiet.configs')
        self._parent_ingredient: 'Ingredient' = parent_ingredient
        self._child_nutrient_amounts: Dict[str, 'NutrientAmount'] = {}
        self._parent_nutrient_amounts: Dict[str, 'NutrientAmount'] = {}
        # If I have child nutrients, then populate those;
        if self.name in self._cf.NUTRIENT_GROUP_DEFINITIONS.keys():
            # For each of my constituents;
            for cn_name in self._cf.NUTRIENT_GROUP_DEFINITIONS[name]:
                # Has its object been instantiated on the parent already?
                if cn_name in self._parent_ingredient._nutrient_amounts.keys():
                    cn = self._parent_ingredient.get_nutrient_amount(cn_name)
                    # Yes, add its reference to my list;
                    self._child_nutrient_amounts[cn_name] = cn
                    # And add myself to its list of parent nutrient amounts;
                    cn._parent_nutrient_amounts[self.name] = self
                # It hasn't, create its object and add it to me and my parent;
                else:
                    # Instantiate;
                    cn = NutrientAmount(cn_name, self._parent_ingredient)
                    # Add to master list on parent;
                    self._parent_ingredient._nutrient_amounts[cn_name] = cn
                    # Add to my list of child nutrient amounts;
                    self._child_nutrient_amounts[cn_name] = cn
                    # Add myself to its list of parent nutrient amounts;
                    cn._parent_nutrient_amounts[self.name] = self

    @property
    def defined(self) -> bool:
        data = self._parent_ingredient._data['nutrients'][self.name]
        for field in data:
            if data[field] == None:
                return False
        return True

    @property
    def ingredient_qty(self) -> float:
        return self._parent_ingredient._data['nutrients'][self.name]['ingredient_qty']

    @ingredient_qty.setter
    def ingredient_qty(self, value: float):
        self._safe_set('ingredient_qty', value)

    @property
    def ingredient_qty_units(self) -> str:
        return self._parent_ingredient._data['nutrients'][self.name]['ingredient_qty_units']

    @ingredient_qty_units.setter
    def ingredient_qty_units(self, value: str):
        # Validate the unit;
        self._us.validate_unit(value)
        # Proceed with safe set;
        self._safe_set('ingredient_qty_units', value)

    @property
    def ingredient_qty_g(self) -> float:
        # Check I am defined first;
        if not self.defined:
            raise NutrientAmountUndefinedError
        # If my units are already defined as a mass;
        if self.ingredient_qty_units in self._us.recognised_mass_units():
            return self._us.convert_mass(
                self.ingredient_qty,
                self.ingredient_qty_units,
                'g'
            )
        # My units must be defined as a vol;
        else:
            return self._us.convert_vol_to_grams(
                self.ingredient_qty,
                self.ingredient_qty_units,
                self._parent_ingredient.density_g_per_ml
            )


    @property
    def nutrient_mass(self) -> float:
        return self._parent_ingredient._data['nutrients'][self.name]['nutrient_mass']

    @property
    def nutrient_mass_g(self) -> float:
        return self._us.convert_mass(
            self.nutrient_mass,
            self.nutrient_mass_units,
            'g'
        )

    @nutrient_mass.setter
    def nutrient_mass(self, value: float):
        self._safe_set('nutrient_mass', value)

    @property
    def nutrient_mass_units(self) -> str:
        return self._parent_ingredient._data['nutrients'][self.name]['nutrient_mass_units']

    @nutrient_mass_units.setter
    def nutrient_mass_units(self, value: str):
        # Validate the units;
        self._us.validate_unit(value)
        # Proceed with safe set;
        self._safe_set('nutrient_mass_units', value)

    @property
    def percentage(self) -> float:
        # Catch if I am undefined;
        if not self.defined:
            raise NutrientAmountUndefinedError
        # Convert the nutrient mass to grams;
        nutrient_mass_g = self._us.convert_mass(
            self.nutrient_mass,
            self.nutrient_mass_units,
            'g'
        )
        # If ingredient qty is a mass, convert to grams;
        if self.ingredient_qty_units in self._us.recognised_mass_units():
            ingredient_mass_g = self._us.convert_mass(
                self.ingredient_qty,
                self.ingredient_qty_units,
                'g'
            )
        # If ingredient qty is a vol, convert to grams;
        else:
            ingredient_mass_g = self._us.convert_vol_to_grams(
                self.ingredient_qty,
                self.ingredient_qty_units,
                self._parent_ingredient.density_g_per_ml
            )
        #
        return (nutrient_mass_g/ingredient_mass_g)*100

    def _safe_set(self, field_name:str, value:Union[str, float])->None:
        # Take a backup in case the new data invalidates me;
        backup = self._parent_ingredient._data['nutrients'][self.name].copy()
        # Set the new data;
        self._parent_ingredient._data['nutrients'][self.name][field_name] = value
        # If I am defined, check my validity;
        if self.defined:
            try:
                self.validate()
            # If I am now invalid, reset the old data and pass the exception on;
            except (
                NutrientQtyExceedsIngredientQtyError, 
                ConstituentsExceedGroupError) as e:
                self._parent_ingredient._data['nutrients'][self.name] = backup
                raise e

    def validate(self):
        # Check I am defined;
        if not self.defined:
            raise NutrientAmountUndefinedError
        # Check nutrient qty does not exceed ingredient qty;
        nut_mass_g = self._us.convert_mass(
            self.nutrient_mass, self.nutrient_mass_units, 'g'
        )
        if nut_mass_g > self.ingredient_qty_g:
            raise NutrientQtyExceedsIngredientQtyError('The quantity of {} cannot exceed the mass of the ingredient containing it'.format(self.name)
            )
        # If I am a child nutrient;
        if len(self._parent_nutrient_amounts):
            # For each parent nutrient group I am part of;
            for pna in self._parent_nutrient_amounts.values():
                # If the parent is defined;
                if pna.defined:
                    # Sum mine & sibling percentages;
                    sibling_perc_sum = self.percentage # starting with mine;
                    for sibling in pna._child_nutrient_amounts.values():
                        if sibling.defined:
                            sibling_perc_sum = sibling_perc_sum + sibling.percentage
                    # Raise exception if sibling sum exceed parent sum;
                    if sibling_perc_sum > pna.percentage:
                        raise ConstituentsExceedGroupError('The combined {group} cannot exceed the total {group}'.format(group=pna.name))
