from typing import Optional, Dict, List

from pydiet.nutrients import nutrient_amount
from pydiet import nutrients
from pydiet.ingredients.exceptions import IngredientDensityUndefinedError
from pydiet import configs as cfg
from pydiet.units import units_service as us
from pydiet.ingredients import ingredient_service as igs

DATA_TEMPLATE = {
  "cost_per_mass": {
    "cost": None,
    "ingredient_qty": None,
    "ingredient_qty_units": None
  },
  "flags": {},
  "name": None,
  "nutrients": {},
  "vol_density": {
    "ingredient_mass": None,
    "ingredient_mass_units": None,
    "ingredient_vol": None,
    "ingredient_vol_units": None
  }
}

class Ingredient():
    def __init__(self, data):
        self._data = data
        self._nutrient_amounts: Dict[str, 'nutrient_amount.NutrientAmount'] = {}
        # Instantiate the nutrient amounts;
        for na_name in data['nutrients'].keys():
            if not na_name in self._nutrient_amounts.keys():
                self._nutrient_amounts[na_name] = nutrient_amount.NutrientAmount(na_name, self)

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
    def cost_per_g(self) -> float:
        # If ingredient qty is a mass;
        if self.cost_data['ingredient_qty_units'] in us.recognised_mass_units():
            return self._data['cost_per_mass']['cost']/us.convert_mass_units(
                self._data['cost_per_mass']['ingredient_qty'],
                self._data['cost_per_mass']['ingredient_qty_units'], "g"            
            )
        # Ingredient qty is a volume;
        else:
            return self._data['cost_per_mass']['cost']/us.convert_volume_to_mass(
                self._data['cost_per_mass']['ingredient_qty'],
                self._data['cost_per_mass']['ingredient_qty_units'],
                'g',
                self.density_g_per_ml         
            )

    @property
    def cost_data(self) -> Dict:
        return self._data['cost_per_mass']

    def set_cost(self, cost: float, mass: float, mass_units: str) -> None:
        # Parse the qty units;
        mass_units = us.parse_qty_unit(mass_units)
        # Set the data;
        self._data['cost_per_mass']['cost'] = cost
        self._data['cost_per_mass']['ingredient_qty'] = mass
        self._data['cost_per_mass']['ingredient_qty_units'] = mass_units

    @property
    def density_is_defined(self)->bool:
        for key in self._data['vol_density'].keys():
            if not self._data['vol_density'][key]:
                return False
        return True

    @property
    def density_g_per_ml(self)->float:
        # Catch density not being defined;
        if not self.density_is_defined:
            raise IngredientDensityUndefinedError
        # Convert mass component to grams;
        mass_g = us.convert_mass_units(
            self._data['vol_density']['ingredient_mass'],
            self._data['vol_density']['ingredient_mass_units'],
            'g'
        )
        # Convert vol component to ml;
        vol_ml = us.convert_volume_units(
            self._data['vol_density']['ingredient_vol'],
            self._data['vol_density']['ingredient_vol_units'],
            'ml'
        )
        # Return g/ml;
        return mass_g/vol_ml

    def set_density(
        self, ingredient_vol: float,
        ingredient_vol_units: str,
        ingredient_mass: float,
        ingredient_mass_units: str
    ) -> None:
        # Interpret the units;
        ingredient_mass_units = us.parse_qty_unit(ingredient_mass_units)
        ingredient_vol_units = us.parse_qty_unit(ingredient_vol_units)
        # Set the units;
        self._data['vol_density']['ingredient_mass'] = ingredient_mass
        self._data['vol_density']['ingredient_mass_units'] = ingredient_mass_units
        self._data['vol_density']['ingredient_vol'] = ingredient_vol
        self._data['vol_density']['ingredient_vol_units'] = ingredient_vol_units

    @property
    def all_flag_data(self) -> Dict:
        return self._data['flags']

    @property
    def all_flags_undefined(self) -> bool:
        for flag_name in self.all_flag_data:
            if not self.all_flag_data[flag_name] == None:
                return False
        return True

    def flag_is_defined(self, flag_name)->bool:
        if self.all_flag_data[flag_name] == None:
            return False
        else:
            return True

    def set_flag(self, flag_name: str, value: bool) -> None:
        # Reference the nutrient-flag relations;
        nfls = nutrients.configs.NUTRIENT_FLAG_RELS
        # Set the flag;
        self.all_flag_data[flag_name] = value
        # Update any associated nutrients;
        if value and flag_name in nfls.keys():
            for assoc_nutr_name in nfls[flag_name]:
                self.set_nutrient_amount(assoc_nutr_name, 100, 'g', 0, 'g')


    def get_flag(self, flag_name: str) -> Optional[bool]:
        return self._data['flags'][flag_name]

    @property
    def primary_nutrients(self)->Dict[str, 'nutrient_amount.NutrientAmount']:
        primary_nutrients = {}
        for pn in nutrients.configs.PRIMARY_NUTRIENTS:
            primary_nutrients[pn] = self.get_nutrient_amount(pn)
        return primary_nutrients

    @property
    def secondary_nutrients(self)->Dict[str, 'nutrient_amount.NutrientAmount']:
        secondary_nutrients = {}
        all_nutrient_names = igs.get_all_nutrient_names()
        for nn in all_nutrient_names:
            if not nn in nutrients.data_templates.PRIMARY_NUTRIENTS:
                secondary_nutrients[nn] = self.get_nutrient_amount(nn)
        return secondary_nutrients

    @property
    def defined_secondary_nutrients(self)->Dict[str, 'nutrient_amount.NutrientAmount']:
        dsn = {} # defined secondary nutreints
        secondary_nutrients = self.secondary_nutrients
        for snn in secondary_nutrients.keys():
            if secondary_nutrients[snn].defined:
                dsn[snn] = secondary_nutrients[snn]
        return dsn

    def set_nutrient_amount(
        self,
        nutrient_name: str,
        ingredient_qty: float,
        ingredient_qty_units: str,
        nutrient_mass: float,
        nutrient_mass_units: str,) -> None:
        na = self.get_nutrient_amount(nutrient_name)
        na.ingredient_qty = ingredient_qty
        na.ingredient_qty_units = ingredient_qty_units
        na.nutrient_mass = nutrient_mass
        na.nutrient_mass_units = nutrient_mass_units

    def get_nutrient_amount(self, nutrient_name) -> 'nutrient_amount.NutrientAmount':
        return self._nutrient_amounts[nutrient_name]

    def validate(self):
        # Call validate on all constituent nutrients;
        for nutrient_amount in self._nutrient_amounts.values():
            nutrient_amount.validate()
        # TODO - Also check that the percentage sum of all constituents
        # does not exceed 100%, but be careful not to count molecules
        # and groups twice as some molecules may be part of different
        # groups - careful approach needed here.

    @property
    def defined(self)->bool:
        if len(self.missing_mandatory_attrs):
            return False
        else:
            return True

    @property
    def missing_mandatory_attrs(self)->List[str]:
        # Init list of missing attrs to return;
        missing_attrs = []
        # Check name;
        if not self.name:
            missing_attrs.append('name')
        # Check cost;
        if not self.cost_is_defined:
            missing_attrs.append('cost')
        # Check flags;
        flag_data = self.all_flag_data
        for flag_name in flag_data.keys():
            if not self.flag_is_defined(flag_name):
                missing_attrs.append(flag_name.replace('_', ' ') +' flag')
        # Check nutrients;
        for nutrient in self.primary_nutrients.values():
            if not nutrient.defined:
                missing_attrs.append(nutrient.name)
        # Return list of missing attrs;
        return missing_attrs

