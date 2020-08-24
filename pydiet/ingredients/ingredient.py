from typing import Optional, Dict, List, Union

from pydiet import nutrients, defining, quantity, cost, flags, quantity

data_template = {
  "cost_per_mass": {},
  "flags": {},
  "name": None,
  "nutrients": {},
  "vol_density": {}
}

class Ingredient(
        defining.i_needs_defining.INeedsDefining,
        cost.i_has_cost.IHasCost,
        flags.i_has_flags.IHasFlags,
        nutrients.i_has_nutrient_amounts.IHasNutrientAmounts,
        quantity.i_has_density.IHasDensity):

    def __init__(self, data):
        self._data = data
        self._nutrient_amounts: Dict[str,
                                     'nutrients.nutrient_amount.NutrientAmount'] = {}
        # Instantiate the nutrient amounts;
        for na_name in data['nutrients'].keys():
            if not na_name in self._nutrient_amounts.keys():
                self._nutrient_amounts[na_name] = nutrients.nutrient_amount.NutrientAmount(
                    na_name, self)

    @property
    def missing_mandatory_attrs(self) -> List[str]:
        # Init list of missing attrs to return;
        missing_attrs = []
        # Check name;
        if self.name == None:
            missing_attrs.append('name')
        # Check cost;
        if not self.cost_is_defined:
            missing_attrs.append('cost')
        # Check flags;
        flag_data = self.flags
        for flag_name in flag_data.keys():
            if not self.flag_is_defined(flag_name):
                missing_attrs.append(flag_name.replace('_', ' ') + ' flag')
        # Check nutrients;
        for nutrient in self.primary_nutrients.values():
            if not nutrient.defined:
                missing_attrs.append(nutrient.name)
        # Return list of missing attrs;
        return missing_attrs

    @property
    def name(self) -> Optional[str]:
        return self._data['name']

    @name.setter
    def name(self, value: str) -> None:
        self._data['name'] = value

    @property
    def cost_data(self) -> Dict[str, Union[str, float]]:
        return self._data['cost_per_mass']

    def set_cost(self, cost: float, qty: float, qty_unit: str) -> None:
        # Validate things;
        qty_unit = quantity.quantity_service.validate_qty_unit(qty_unit)
        cost = float(cost)
        qty = float(qty)
        # Set the data;
        self._data['cost_per_mass']['cost'] = cost
        self._data['cost_per_mass']['qty'] = qty
        self._data['cost_per_mass']['qty_units'] = qty_unit

    @property
    def density_data(self) -> Dict[str, Union[str, float]]:
        return self._data['vol_density']

    def set_density(
        self, vol: float,
        vol_units: str,
        mass: float,
        mass_units: str) -> None:
        # Validate things;
        mass_units = quantity.quantity_service.validate_mass_unit(mass_units)
        vol_units = quantity.quantity_service.validate_vol_unit(vol_units)
        # Set the units;
        data = self.density_data
        data['mass'] = mass
        data['mass_units'] = mass_units
        data['vol'] = vol
        data['vol_units'] = vol_units

    @property
    def flags(self) -> Dict[str, Union[bool, None]]:
        return self._data['flags']

    def set_flag(self, flag_name: str, flag_status: bool) -> None:
        # Reference nutrient-flag relationship lookup;
        nfls = nutrients.configs.nutrient_flag_relationships
        # Set the flag;
        self.flags[flag_name] = flag_status
        # Zero any associated nutrients, to indicate '.....-free';
        if flag_status and flag_name in nfls.keys():
            for assoc_nutr_name in nfls[flag_name]:
                self.set_nutrient_amount(assoc_nutr_name, 100, 'g', 0, 'g')

    def get_nutrient_amount(self, nutrient_name) -> 'nutrients.nutrient_amount.NutrientAmount':
        return self._nutrient_amounts[nutrient_name]

    def validate(self):
        # Call validate on all constituent nutrients;
        for nutrient_amount in self._nutrient_amounts.values():
            nutrient_amount.validate()
        # TODO - Also check that the percentage sum of all constituents
        # does not exceed 100%, but be careful not to count molecules
        # and groups twice as some molecules may be part of different
        # groups - careful approach needed here.
