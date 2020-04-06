from typing import TYPE_CHECKING, Union, Optional, Dict

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
        self.category: str
        self.name = name
        self.parent_ingredient: 'Ingredient' = parent_ingredient
        if self.is_group:
            self.category = 'groups'
        else:
            self.category = 'molecules'

    @property
    def defined(self) -> bool:
        data = self.parent_ingredient._data[self.category][self.name]
        for field in data:
            if data[field] == None:
                return False
        return True

    @property
    def is_group(self) -> bool:
        configs: 'configs' = inject('pydiet.configs')
        if self.name in configs.NUTRIENT_GROUP_DEFINITIONS.keys():
            return True
        else:
            return False

    @property
    def ingredient_mass(self) -> float:
        return self.parent_ingredient._data[self.category][self.name]['ingredient_mass']

    @ingredient_mass.setter
    def ingredient_mass(self, value: float):
        self.parent_ingredient._data[self.category][self.name]['ingredient_mass'] = value
        if self.defined:
            self.validate()

    @property
    def ingredient_mass_units(self) -> str:
        return self.parent_ingredient._data[self.category][self.name]['ingredient_mass_units']

    @ingredient_mass_units.setter
    def ingredient_mass_units(self, value: str):
        self.parent_ingredient._data[self.category][self.name]['ingredient_mass_units'] = value
        if self.defined:
            self.validate()

    @property
    def nutrient_mass(self) -> float:
        return self.parent_ingredient._data[self.category][self.name]['nutrient_mass']

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
        self.parent_ingredient._data[self.category][self.name]['nutrient_mass'] = value
        if self.defined:
            self.validate()

    @property
    def nutrient_mass_units(self) -> str:
        return self.parent_ingredient._data[self.category][self.name]['nutrient_mass_units']

    @nutrient_mass_units.setter
    def nutrient_mass_units(self, value: str):
        self.parent_ingredient._data[self.category][self.name]['nutrient_mass_units'] = value
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
        # Check that the total nutrient mass
        # does not exceed the ingredient mass
        us: 'UtilityService' = inject('pydiet.utility_service')
        nut_mass_g = us.convert_mass(
            self.nutrient_mass, self.nutrient_mass_units, 'g'
        )
        ing_mass_g = us.convert_mass(
            self.ingredient_mass, self.ingredient_mass_units, 'g'
        )
        if nut_mass_g > ing_mass_g:
            raise NutrientQtyExceedsIngredientQtyError


class MoleculeAmount(NutrientAmount):
    def __init__(
        self,
        name: str,
        parent_ingredient: 'Ingredient'
    ):
        super().__init__(name, parent_ingredient)


class GroupAmount(NutrientAmount):
    def __init__(
        self,
        name: str,
        parent_ingredient
    ):
        super().__init__(name, parent_ingredient)
        self.group_amounts: Dict[str, 'GroupAmount'] = {}
        self.molecule_amounts: Dict[str, 'MoleculeAmount'] = {}
        # Unpack the constituents;
        configs: 'configs' = inject('pydiet.configs')
        for constituent_name in configs.NUTRIENT_GROUP_DEFINITIONS[name]:
            # If the constituent is a group;
            if constituent_name in configs.NUTRIENT_GROUP_DEFINITIONS.keys():
                # If the constituent is already instantiated on the parent;
                if constituent_name in self.parent_ingredient.group_amounts.keys():
                    # Add a reference to it;
                    self.group_amounts[constituent_name] = \
                        self.parent_ingredient.group_amounts[constituent_name]
                # If it isn't instantiated yet;
                else:
                    # Instantiate it;
                    self.parent_ingredient.group_amounts[constituent_name] = \
                        GroupAmount(constituent_name, parent_ingredient)
                    # Then add a reference to it;
                    self.group_amounts[constituent_name] = \
                        self.parent_ingredient.group_amounts[constituent_name]
            # Otherwise, the constituent was a molecule, so just add it;
            else:
                self.molecule_amounts[constituent_name] = \
                    self.parent_ingredient.molecule_amounts[constituent_name]

    @property
    def nutrient_amounts(self) -> Dict[str, Union['GroupAmount', 'MoleculeAmount']]:
        all_nutrients = {}
        all_nutrients.update(self.group_amounts)
        all_nutrients.update(self.molecule_amounts)
        return all_nutrients

    def validate(self):
        # Check no basic error with own direct definition;
        super().validate()
        # Check own nutrients don't exceed own stated mass;
        perc_occupied = 0
        for nutrient_amount in self.nutrient_amounts.values():
            if nutrient_amount.defined:
                perc_occupied = perc_occupied + nutrient_amount.percentage
        if perc_occupied > 100:
            raise NutrientQtyExceedsIngredientQtyError


class Ingredient():
    def __init__(self, data):
        self._data = data
        self.group_amounts: Dict[str, 'GroupAmount'] = {}
        self.molecule_amounts: Dict[str, 'MoleculeAmount'] = {}
        # Unpack the molecule data;
        for molecule_name in data['molecules'].keys():
            self.molecule_amounts[molecule_name] = MoleculeAmount(
                molecule_name,
                self
            )
        # Unpack the group data;
        for group_name in data['groups'].keys():
            self.group_amounts[group_name] = GroupAmount(
                group_name,
                self
            )

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

    @property
    def nutrient_amounts(self) -> Dict[str, Union['GroupAmount', 'MoleculeAmount']]:
        nutrient_amounts = {}
        nutrient_amounts.update(self.group_amounts)
        nutrient_amounts.update(self.molecule_amounts)
        return nutrient_amounts

    def set_nutrient_amount(
        self,
        nutrient_name:str,
        ingredient_mass:float,
        ingredient_mass_units:str,
        nutrient_mass:float,
        nutrient_mass_units:str,
    )->None:
        na = self.get_nutrient_amount(nutrient_name)
        na.ingredient_mass = ingredient_mass
        na.ingredient_mass_units = ingredient_mass_units
        na.nutrient_mass = nutrient_mass
        na.nutrient_mass_units = nutrient_mass_units

    def get_nutrient_amount(self, nutrient_name)->'NutrientAmount':
        return self.nutrient_amounts[nutrient_name]

    def validate(self):
        # Call validate on all constituent nutrients;
        for nutrient_amount in self.nutrient_amounts.values():
            nutrient_amount.validate()
