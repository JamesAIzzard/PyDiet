from pydiet import ingredients
from typing import TYPE_CHECKING, Union, Optional, Dict

from pinjector import inject

if TYPE_CHECKING:
    from pydiet.utility_service import UtilityService
    from pydiet import configs

class ConstituentsExceedGroupError(ValueError):
    def __init__(self, message=None):
        super().__init__(message)

class DefinedByConstituentsError(ValueError):
    def __init__(self, message=None):
        super().__init__(message)

class Ingredient():
    def __init__(self, data):
        self._data = data
        self._utility_service: 'UtilityService' = inject(
            'pydiet.utility_service')
        self._configs: 'configs' = inject('pydiet.configs')

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
        if self.cost_is_defined:
            conversion_factor = self._utility_service.convert_mass(
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

    def resolve_alias(self, alias: str) -> str:
        # If the name is known without an alias,
        # just return it;
        if alias in self._data['groups'].keys() or \
                alias in self._data['molecules'].keys():
            return alias
        # Otherwise, hunt through the alias list;
        for rootname in self._configs.NUTRIENT_ALIASES.keys():
            if alias in self._configs.NUTRIENT_ALIASES[rootname]:
                return rootname
        # Not found, raise an exception;
        raise KeyError('The nutrient name {} was not recognised'.format(alias))

    @property
    def all_groups_data(self) -> Dict[str, Dict]:
        groups_data = {}
        for group_name in self._data['groups'].keys():
            groups_data[group_name] = self.get_group_data(group_name)
        return groups_data

    @property
    def all_molecules_data(self) -> Dict[str, Dict]:
        return self._data['molecules']

    @property
    def all_nutrients_data(self) -> Dict[str, Dict]:
        all_nutrients = {}
        all_nutrients.update(self.all_groups_data)
        all_nutrients.update(self.all_molecules_data)
        return all_nutrients

    def _check_nutrient_data_is_complete(self, data: Dict) -> bool:
        for field in data.keys():
            if data[field] == None:
                return False
        return True

    def check_nutrient_is_defined(self, nutrient_name: str) -> bool:
        # Resolve alias;
        nutrient_name = self.resolve_alias(nutrient_name)
        # Grab its data;
        nutrient_data = self.get_nutrient_data(nutrient_name)
        # Check the data;
        return self._check_nutrient_data_is_complete(nutrient_data)

    def get_group_data(self, group_name: str) -> Dict[str, Dict]:
        # Resolve any alias;
        group_name = self.resolve_alias(group_name)
        # Grab the raw data against the top level group name;
        group_data = self._data['groups'][group_name]
        # If the group top level data is defined, just return it;
        if self._check_nutrient_data_is_complete(group_data):
            return group_data
        # Otherwise, check to see if each of its constituents are defined;
        rolling_total = 0
        for constituent_name in self._configs.NUTRIENT_GROUP_DEFINITIONS[group_name]:
            constituent_data = self.get_nutrient_data(constituent_name)
            if self._check_nutrient_data_is_complete(constituent_data):
                rolling_total = rolling_total + \
                    self._calculate_percentage_from_nutrient_data(
                        constituent_data)
            else:
                # Was not defined, so just return the original data with
                # null fields;
                return group_data
        # We were able to complete the rolling total, so the group data;
        # We summed percentages, so use 100g as ingredient qty;
        group_data['ingredient_mass'] = 100
        group_data['ingredient_mass_units'] = 'g'
        group_data['nutrient_mass'] = rolling_total
        group_data['nutrient_mass_units'] = 'g'
        return group_data

    def get_molecule_data(self, molecule_name: str) -> Dict[str, Dict]:
        # Resolve any alias';
        molecule_name = self.resolve_alias(molecule_name)
        # Return the data;
        return self._data['molecules'][molecule_name]

    def get_nutrient_data(self, nutrient_name: str) -> Dict:
        # Convert to root name;
        nutrient_name = self.resolve_alias(nutrient_name)
        # If a molecule name;
        if nutrient_name in self._data['molecules'].keys():
            return self.get_molecule_data(nutrient_name)
        # Otherwise must be a group or resolve alias would
        # have thrown exception;
        else:
            return self.get_group_data(nutrient_name)

    def set_molecule_data(
        self, 
        molecule_name: str,
        molecule_mass: float, 
        molecule_mass_units: str,
        ingredient_mass: float,
        ingredient_mass_units: str
    )->None:
        # Resolve any alias;
        molecule_name = self.resolve_alias(molecule_name)
        # Save data in case invalidates;
        old_data = self.get_molecule_data(molecule_name)
        # Set the new data;
        self._data['molecules'][molecule_name]['ingredient_mass'] = ingredient_mass
        self._data['molecules'][molecule_name]['ingredient_mass_units'] = ingredient_mass_units
        self._data['molecules'][molecule_name]['nutrient_mass'] = molecule_mass
        self._data['molecules'][molecule_name]['nutrient_mass_units'] = molecule_mass_units        
        # Check it validates;
        try:
            self.validate()
        # If it doesn't, reset the old data and pass the error on;
        except ConstituentsExceedGroupError as e:
            self._data['molecules'][molecule_name] = old_data
            raise e

    def set_group_data(
        self, 
        group_name: str,
        group_mass: float, 
        group_mass_units: str,
        ingredient_mass: float,
        ingredient_mass_units: str
    )->None:
        # Resolve alias;
        group_name = self.resolve_alias(group_name)
        # Save the old data in case it invalidates;
        old_data = self.get_group_data(group_name)
        # If the group is full defined by its constituents,
        # dissalow setting, set constituents instead.
        if self._are_constituents_defined(group_name):
            raise DefinedByConstituentsError('The nutrient {} is fully defined by its constituents and cannot be set directly.')
        # Else it is not fully defined, so set.
        else:
            self._data['groups'][group_name]['ingredient_mass'] = ingredient_mass
            self._data['groups'][group_name]['ingredient_mass_units'] = ingredient_mass_units
            self._data['groups'][group_name]['nutrient_mass'] = group_mass
            self._data['groups'][group_name]['nutrient_mass_units'] = group_mass_units
        # Now check validity in case the constituent sum now
        # exceeds the group value;
        try:
            self.validate()
        # The incomplete set of constituents still exceeds the group total,
        # so replace the data and pass on exception;
        except ConstituentsExceedGroupError as e:
            self._data['groups'][group_name] = old_data
            raise e

    def set_nutrient_data(
        self, 
        nutrient_name: str,
        nutrient_mass: float, 
        nutrient_mass_units: str,
        ingredient_mass: float,
        ingredient_mass_units: str
    ) -> None:
        nutrient_name = self.resolve_alias(nutrient_name)
        # If the nutrient is a molecule;
        if nutrient_name in self._data['molecules'].keys():
            # Go ahead and set it;
            self.set_molecule_data(
                nutrient_name, nutrient_mass, nutrient_mass_units,
                ingredient_mass, ingredient_mass_units
            )
        # Otherwise, nutrient is a group;
        # TODO
 
    
    def _are_constituents_defined(self, group_name:str)->bool:
        group_name = self.resolve_alias(group_name)
        for constituent_name in self.all_groups_data.keys():
            if not self.check_nutrient_is_defined(constituent_name):
                return False
        return True

    def get_nutrient_percentage(self, nutrient_name: str) -> float:
        nutrient_data = self.get_nutrient_data(nutrient_name)
        return self._calculate_percentage_from_nutrient_data(nutrient_data)

    def _calculate_percentage_from_nutrient_data(self, data: Dict) -> float:
        nutrient_mass_in_grams = self._utility_service.convert_mass(
            data['mass'], data['mass_units'], 'g'
        )
        sample_mass_in_grams = self._utility_service.convert_mass(
            data['mass_per'], data['mass_per_units'], 'g'
        )
        return (nutrient_mass_in_grams/sample_mass_in_grams)*100
