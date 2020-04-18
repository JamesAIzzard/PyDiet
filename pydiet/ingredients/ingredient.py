from typing import TYPE_CHECKING, Union, Optional, Dict, List

from pinjector import inject

if TYPE_CHECKING:
    from pydiet import configs
    from pydiet import utility_service


class NutrientQtyExceedsIngredientQtyError(ValueError):
    def __init__(self, *args):
        if args[0]:
            super().__init__(args[0])


class ConstituentsExceedGroupError(ValueError):
    def __init__(self, *args):
        if args[0]:
            super().__init__(args[0])


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
                # Check that the sum of the sibling percentages in this group
                # do not exceed the parent's percentage;
<<<<<<< HEAD
                sibling_perc_sum = 0
=======
                parent_perc = pna.percentage
                sibling_perc_sum = 0 
>>>>>>> 503b965f49ec6f9fb2d332ffe5e296d7bb0354fd
                for sibling in pna._child_nutrient_amounts.values():
                    if sibling.defined:
                        sibling_perc_sum = sibling_perc_sum + sibling.percentage
                if sibling_perc_sum > parent_perc:
                    raise ConstituentsExceedGroupError('The constituents of {} sum to {}% more than the stated % for {} in {}'.format(
                        pna.name, sibling_perc_sum-parent_perc, pna.name, self._parent_ingredient.name))


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
        ut: 'utility_service' = inject('pydiet.utility_service')
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

    def set_density(
        self, vol: float,
        vol_units: str,
        mass_per_vol: float,
        mass_per_vol_units: str
    ) -> None:
        self._data['vol_density']['ingredient_mass']
        self._data['vol_density']['ingredient_mass_units']
        self._data['vol_density']['ingredient_vol']
        self._data['vol_density']['ingredient_vol_units']

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
