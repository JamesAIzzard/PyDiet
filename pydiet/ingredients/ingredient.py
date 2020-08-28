from typing import Optional, Dict, List, Union

from pydiet import nutrients, defining, quantity, cost, flags, quantity

data_template = {
    "cost": {},
    "flags": {},
    "name": None,
    "nutrients": {},
    "density": {}
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
        for nutrient in self.primary_nutrient_amounts.values():
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
    def readonly_cost_data(self) -> Dict[str, Union[str, float]]:
        return self._data['cost'].copy()

    def set_cost(self, cost: float, mass_g: float, pref_qty_units: str) -> None:
        # Validate things;
        pref_qty_units = quantity.quantity_service.validate_qty_unit(pref_qty_units)
        cost = float(cost)
        mass_g = float(mass_g)
        # Set the data;
        self._data['cost']['cost'] = cost
        self._data['cost']['mass_g'] = mass_g
        self._data['cost']['pref_qty_units'] = pref_qty_units

    @property
    def readonly_density_data(self) -> Dict[str, Union[float, str]]:
        return self._data['density'].copy()

    def set_density(self, g_per_ml:float, pref_vol_units:str):
        g_per_ml = quantity.quantity_service.validate_density(g_per_ml)
        pref_vol_units = quantity.quantity_service.validate_vol_unit(pref_vol_units)
        self._data['density']['g_per_ml'] = g_per_ml
        self._data['density']['pref_vol_units'] = pref_vol_units

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

    @property
    def nutrient_amounts(self) -> Dict[str, 'nutrients.nutrient_amount.NutrientAmount']:
        return self._nutrient_amounts

    def get_readonly_nutrient_amount_data(self, nutrient_name: str) -> Dict[str, Union[float, str]]:
        return self._data['nutrients'][nutrient_name].copy()

    def set_nutrient_amount(self,
                            nutrient_name:str,
                            self_mass_g: float,
                            self_qty_pref_units:str,
                            nutrient_mass_g:float,
                            nutrient_qty_pref_units:str) -> None:
        # Get a reference to the data, and a backup;
        data = self._data['nutrients'][nutrient_name]
        backup_data = data.copy()
        
        # Make the changes;
        data['parent_mass_g'] = self_mass_g
        data['parent_qty_pref_units'] = self_qty_pref_units
        data['nutrient_mass_g'] = nutrient_mass_g
        data['nutrient_qty_pref_units'] = nutrient_qty_pref_units

        # Revert if validation fails;
        try:
            self._validate_nutrient_amounts()
        except nutrients.exceptions.InvalidNutrientAmountsError as e:
            self._data['nutrients'][nutrient_name] = backup_data
            raise e
        
        # TODO - Make any implied flag updates;

    def _validate_nutrient_amounts(self):
        raise NotImplementedError