from typing import TYPE_CHECKING, Union, Optional, Dict, List

from pinjector import inject

from pydiet.ingredients.nutrient_amount import NutrientAmount

if TYPE_CHECKING:
    from pydiet.shared import configs
    from pydiet.shared import utility_service

class Ingredient():
    def __init__(self, data):
        self._ut:'utility_service' = inject('pydiet.utility_service')
        self._cf:'configs' = inject('pydiet.configs')
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

    @property
    def density_is_defined(self)->bool:
        for key in self._data['vol_density'].keys():
            if not self._data['vol_density'][key]:
                return False
        return True

    @property
    def density_g_per_ml(self)->Optional[float]:
        if self.density_is_defined:
            mass_g = self._ut.convert_mass(
                self._data['vol_density']['ingredient_mass'],
                self._data['vol_density']['ingredient_mass_units'],
                'g'
            )
            vol_ml = self._ut.convert_volume(
                self._data['vol_density']['ingredient_vol'],
                self._data['vol_density']['ingredient_vol_units'],
                'ml'
            )
            return mass_g/vol_ml
        else:
            return None

    def set_density(
        self, ingredient_vol: float,
        ingredient_vol_units: str,
        ingredient_mass: float,
        ingredient_mass_units: str
    ) -> None:
        # Lowercase the units;
        ingredient_vol_units = ingredient_vol_units.lower()
        ingredient_mass_units = ingredient_mass_units.lower()
        # Check the units;
        if not ingredient_vol_units in self._ut.recognised_vol_units():
            raise ValueError('{} is not a recognised unit of volume.'.format(ingredient_vol_units))
        if not ingredient_mass_units in self._ut.recognised_mass_units():
            raise ValueError('{} is not a recognised unit of mass.'.format(ingredient_mass_units))
        # Set the units;
        self._data['vol_density']['ingredient_mass'] = ingredient_mass
        self._data['vol_density']['ingredient_mass_units'] = ingredient_mass_units.lower()
        self._data['vol_density']['ingredient_vol'] = ingredient_vol
        self._data['vol_density']['ingredient_vol_units'] = ingredient_vol_units.lower()

    def convert_vol_to_grams(self, volume:float, units:str)->float:
        # Lowercase units;
        units = units.lower()
        # First convert the volume to ml;
        vol_ml = self._ut.convert_volume(volume, units, 'ml')
        # Calculate mass in g;
        mass_g = self.density_g_per_ml*vol_ml
        return mass_g

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
    def primary_nutrients(self)->Dict[str, 'NutrientAmount']:
        primary_nutrients = {}
        for pn in self._cf.PRIMARY_NUTRIENTS:
            primary_nutrients[pn] = self.get_nutrient_amount(pn)
        return primary_nutrients

    @property
    def secondary_nutrients(self)->Dict[str, 'NutrientAmount']:
        secondary_nutrients = {}
        all_nutrient_names = self._ut.get_all_nutrient_names()
        for nn in all_nutrient_names:
            if not nn in self._cf.PRIMARY_NUTRIENTS:
                secondary_nutrients[nn] = self.get_nutrient_amount(nn)
        return secondary_nutrients

    @property
    def defined_secondary_nutrients(self)->Dict[str, 'NutrientAmount']:
        dsn = {} # defined secondary nutreints
        secondary_nutrients = self.secondary_nutrients
        for snn in secondary_nutrients.keys():
            if secondary_nutrients[snn].defined:
                dsn[snn] = secondary_nutrients[snn]
        return dsn

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
        na.ingredient_mass_units = ingredient_mass_units.lower()
        na.nutrient_mass = nutrient_mass
        na.nutrient_mass_units = nutrient_mass_units.lower()

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
