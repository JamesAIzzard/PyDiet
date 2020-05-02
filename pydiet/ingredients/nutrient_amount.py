from typing import TYPE_CHECKING, Dict, Optional, Union

from pinjector import inject

from pydiet.ingredients.exceptions import (
    NutrientQtyExceedsIngredientQtyError,
    ConstituentsExceedGroupError
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
        self._utility_service:'utility_service' = inject('pydiet.utility_service')
        self._parent_ingredient: 'Ingredient' = parent_ingredient
        self._child_nutrient_amounts: Dict[str, 'NutrientAmount'] = {}
        self._parent_nutrient_amounts: Dict[str, 'NutrientAmount'] = {}
        # Inject some useful services;
        cf: 'configs' = inject('pydiet.configs')
        # If I have child nutrients, then populate those;
        if self.name in cf.NUTRIENT_GROUP_DEFINITIONS.keys():
            # For each of my constituents;
            for cn_name in cf.NUTRIENT_GROUP_DEFINITIONS[name]:
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
    def ingredient_mass(self) -> float:
        return self._parent_ingredient._data['nutrients'][self.name]['ingredient_mass']

    @ingredient_mass.setter
    def ingredient_mass(self, value: float):
        self._safe_set('ingredient_mass', value)

    @property
    def ingredient_mass_units(self) -> str:
        return self._parent_ingredient._data['nutrients'][self.name]['ingredient_mass_units']

    @ingredient_mass_units.setter
    def ingredient_mass_units(self, value: str):
        # Validate the unit;
        self._utility_service.validate_unit(value)
        # Proceed with safe set;
        self._safe_set('ingredient_mass_units', value)

    @property
    def nutrient_mass(self) -> float:
        return self._parent_ingredient._data['nutrients'][self.name]['nutrient_mass']

    @property
    def nutrient_mass_g(self) -> Optional[float]:
        if not self.nutrient_mass == None \
                and not self.nutrient_mass_units == None:
            ut: 'utility_service' = inject('pydiet.utility_service')
            return ut.convert_mass(
                self.nutrient_mass,
                self.nutrient_mass_units,
                'g'
            )
        else:
            return None

    @nutrient_mass.setter
    def nutrient_mass(self, value: float):
        self._safe_set('nutrient_mass', value)

    @property
    def nutrient_mass_units(self) -> str:
        return self._parent_ingredient._data['nutrients'][self.name]['nutrient_mass_units']

    @nutrient_mass_units.setter
    def nutrient_mass_units(self, value: str):
        # Validate the units;
        self._utility_service.validate_unit(value)
        # Proceed with safe set;
        self._safe_set('nutrient_mass_units', value)

    @property
    def percentage(self) -> Optional[float]:
        if self.defined:
            ut: 'utility_service' = inject('pydiet.utility_service')
            nutrient_mass_g = ut.convert_mass(
                self.nutrient_mass,
                self.nutrient_mass_units,
                'g'
            )
            ingredient_mass_g = ut.convert_mass(
                self.ingredient_mass,
                self.ingredient_mass_units,
                'g'
            )
            return (nutrient_mass_g/ingredient_mass_g)*100
        else:
            return None

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
        # Basic check to ensure my nutrient qty does not excced
        # its respective ingredient quantity;
        nut_mass_g = self._utility_service.convert_mass(
            self.nutrient_mass, self.nutrient_mass_units, 'g'
        )
        ing_mass_g = self._utility_service.convert_mass(
            self.ingredient_mass, self.ingredient_mass_units, 'g'
        )
        if nut_mass_g > ing_mass_g:
            raise NutrientQtyExceedsIngredientQtyError('The quantity of {} cannot exceed the mass of the ingredient containing it'.format(self.name)
            )
        # If I am a child nutrient, check that the sum of mine and
        # my siblings values do not exceed parent's percentage;
        if len(self._parent_nutrient_amounts):
            # For each of the groups this nutrient is in;
            for pna in self._parent_nutrient_amounts.values():
                # If the parent is defined;
                if pna.defined:
                    # Check that the sum of the sibling percentages in this group
                    # do not exceed the parent's percentage;
                    parent_perc = pna.percentage
                    sibling_perc_sum = 0 
                    for sibling in pna._child_nutrient_amounts.values():
                        if sibling.defined:
                            sibling_perc_sum = sibling_perc_sum + sibling.percentage
                    if sibling_perc_sum > parent_perc:
                        raise ConstituentsExceedGroupError('The combined {group} cannot exceed the total {group}'.format(group=pna.name))
