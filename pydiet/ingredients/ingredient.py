from typing import TYPE_CHECKING, Union, Optional, Dict, List

from pinjector import inject

if TYPE_CHECKING:
    from pydiet.utility_service import UtilityService
    from pydiet import configs


class NutrientQtyExceedsIngredientQtyError(ValueError):
    def __init__(self, message=None):
        super().__init__(message)


class ConstituentsExceedGroupError(ValueError):
    def __init__(self, message=None):
        super().__init__(message)


class NutrientAmount():
    def __init__(
        self,
        name: str,
        parent_ingredient: 'Ingredient'
    ):
        self.name = name
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
        self._parent_ingredient._data['nutrients'][self.name]['ingredient_mass'] = value
        if self.defined:
            self.validate()

    @property
    def ingredient_mass_units(self) -> str:
        return self._parent_ingredient._data['nutrients'][self.name]['ingredient_mass_units']

    @ingredient_mass_units.setter
    def ingredient_mass_units(self, value: str):
        self._parent_ingredient._data['nutrients'][self.name]['ingredient_mass_units'] = value
        if self.defined:
            self.validate()

    @property
    def nutrient_mass(self) -> float:
        return self._parent_ingredient._data['nutrients'][self.name]['nutrient_mass']

    @property
    def nutrient_mass_g(self) -> Optional[float]:
        if not self.nutrient_mass == None \
                and not self.nutrient_mass_units == None:
            ut: 'UtilityService' = inject('pydiet.utility_service')
            return ut.convert_mass(
                self.nutrient_mass,
                self.nutrient_mass_units,
                'g'
            )
        else:
            return None

    @nutrient_mass.setter
    def nutrient_mass(self, value: float):
        self._parent_ingredient._data['nutrients'][self.name]['nutrient_mass'] = value
        if self.defined:
            self.validate()

    @property
    def nutrient_mass_units(self) -> str:
        return self._parent_ingredient._data['nutrients'][self.name]['nutrient_mass_units']

    @nutrient_mass_units.setter
    def nutrient_mass_units(self, value: str):
        self._parent_ingredient._data['nutrients'][self.name]['nutrient_mass_units'] = value
        if self.defined:
            self.validate()

    @property
    def percentage(self) -> Optional[float]:
        if self.defined:
            ut: 'UtilityService' = inject('pydiet.utility_service')
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

    def validate(self):
        us: 'UtilityService' = inject('pydiet.utility_service')
        cf: 'configs' = inject('pydiet.configs')
        # Basic check to ensure my nutrient qty does not excced
        # its respective ingredient quantity;
        nut_mass_g = us.convert_mass(
            self.nutrient_mass, self.nutrient_mass_units, 'g'
        )
        ing_mass_g = us.convert_mass(
            self.ingredient_mass, self.ingredient_mass_units, 'g'
        )
        if nut_mass_g > ing_mass_g:
            raise NutrientQtyExceedsIngredientQtyError
        # If I am a child nutrient, check that the sum of mine and
        # my siblings values do not exceed parent's percentage;
        if len(self._parent_nutrient_amounts):
            # For each of the groups this nutrient is in;
            for pna in self._parent_nutrient_amounts.values():
                # Check that the sum of the sibling percentages in this group
                # do not exceed the parent's percentage;
                sibling_perc_sum = 0 
                for sibling in pna._child_nutrient_amounts.values():
                    if sibling.defined:
                        sibling_perc_sum = sibling_perc_sum + sibling.percentage
                if sibling_perc_sum > 100:
                    raise ConstituentsExceedGroupError('The constituents of {} sum to {}% in {}'.format(
                        pna.name, sibling_perc_sum, self._parent_ingredient.name))

class Ingredient():
    def __init__(self, data):
        self._data = data
        self._nutrient_amounts: Dict[str, 'NutrientAmount'] = {}
        # Instantiate the nutrient amounts;
        for na_name in data['nutrients'].keys():
            if not na_name in self._nutrient_amounts.keys():
                self._nutrient_amounts[na_name] = NutrientAmount(na_name, self)

    @property
    def name(self) -> str:
        return self._data['name']

    @name.setter
    def name(self, value: str) -> None:
        self._data['name'] = value

    @property
    def cost_is_defined(self) -> bool:
        for key in self._data['cost_per_mass']:
            if not self._data['cost_per_mass'][key]:
                return False
        return True

    @property
    def cost_per_g(self) -> Union[float, None]:
        ut: 'UtilityService' = inject('pydiet.utility_service')
        if self.cost_is_defined:
            conversion_factor = ut.convert_mass(
                self._data['cost_per_mass']['ingredient_mass'],
                self._data['cost_per_mass']['ingredient_mass_units'], "g"
            )
            return self._data['cost_per_mass']['cost']/conversion_factor
        else:
            return None

    @property
    def cost_data(self) -> Dict:
        return self._data['cost_per_mass']

    def set_cost(self, cost: float, mass: float, mass_units: str) -> None:
        self._data['cost_per_mass']['cost'] = cost
        self._data['cost_per_mass']['ingredient_mass'] = mass
        self._data['cost_per_mass']['ingredient_mass_units'] = mass_units

    @property
    def all_flag_data(self) -> Dict:
        return self._data['flags']

    @property
    def all_flags_undefined(self) -> bool:
        for flag_name in self.all_flag_data:
            if not self.all_flag_data[flag_name] == None:
                return False
        return True

    def set_flag(self, flag_name: str, value: bool) -> None:
        self.all_flag_data[flag_name] = value

    def get_flag(self, flag_name: str) -> Optional[bool]:
        return self._data['flags'][flag_name]

    def set_nutrient_amount(
        self,
        nutrient_name: str,
        ingredient_mass: float,
        ingredient_mass_units: str,
        nutrient_mass: float,
        nutrient_mass_units: str,
    ) -> None:
        na = self.get_nutrient_amount(nutrient_name)
        na.ingredient_mass = ingredient_mass
        na.ingredient_mass_units = ingredient_mass_units
        na.nutrient_mass = nutrient_mass
        na.nutrient_mass_units = nutrient_mass_units

    def get_nutrient_amount(self, nutrient_name) -> 'NutrientAmount':
        return self._nutrient_amounts[nutrient_name]

    def validate(self):
        # Call validate on all constituent nutrients;
        for nutrient_amount in self._nutrient_amounts.values():
            nutrient_amount.validate()
        # TODO - Also check that the percentage sum of all constituents
        # does not exceed 100%, but be careful not to count molecules
        # and groups twice as some molecules may be part of different
        # groups - careful approach needed here.
