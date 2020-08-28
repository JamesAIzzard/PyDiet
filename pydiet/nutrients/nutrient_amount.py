from typing import Dict, Union, Optional, cast

from pydiet import nutrients, quantity, flags

data_template = {
    "parent_mass_g": None,
    "parent_qty_pref_units": None,
    "nutrient_mass_g": None,
    "nutrient_qty_pref_units": None
}

class NutrientAmount():
    '''Models the relationship between the quantity of a substance (the parent)
    and the quantities of nutrients it contains.
    '''
    def __init__(
        self,
        name: str,
        parent: 'nutrients.i_has_nutrient_amounts.IHasNutrientAmounts'
    ):
        self._name = name
        self._parent: 'nutrients.i_has_nutrient_amounts.IHasNutrientAmounts' = parent
        self._child_nutrient_amounts: Dict[str, 'NutrientAmount'] = {}
        self._parent_nutrient_amounts: Dict[str, 'NutrientAmount'] = {}

        # If I have child nutrients, then populate those;
        if self.name in nutrients.configs.nutrient_group_definitions.keys():
            # For each of my constituents;
            for constituent_nutrient_name in nutrients.configs.nutrient_group_definitions[self.name]:
                # Has its object been instantiated on the parent already?
                if constituent_nutrient_name in self._parent.nutrient_amounts.keys():
                    constituent_nutrient = self._parent.get_nutrient_amount(constituent_nutrient_name)
                    # Yes, add its reference to my list;
                    self._child_nutrient_amounts[constituent_nutrient_name] = constituent_nutrient
                    # And add myself to its list of parent nutrient amounts;
                    constituent_nutrient._parent_nutrient_amounts[self.name] = self
                # It hasn't, create its object and add it to me and my parent;
                else:
                    # Instantiate;
                    constituent_nutrient = NutrientAmount(constituent_nutrient_name, self._parent)
                    # Add to master list on parent;
                    self._parent.nutrient_amounts[constituent_nutrient_name] = constituent_nutrient
                    # Add to my list of child nutrient amounts;
                    self._child_nutrient_amounts[constituent_nutrient_name] = constituent_nutrient
                    # Add myself to its list of parent nutrient amounts;
                    constituent_nutrient._parent_nutrient_amounts[self.name] = self

    @property
    def name(self)->str:
        return self._name

    @property
    def data(self) -> Dict[str, Union[str, float]]:
        return self._parent.get_readonly_nutrient_amount_data(self.name)

    @property
    def defined(self) -> bool:
        for field in self.data:
            if self.data[field] == None:
                return False
        return True

    @property
    def parent_mass_g(self) -> Optional[float]:
        return cast(Optional[float], self.data['parent_qty_g'])

    @property
    def parent_qty_pref_units(self) -> Optional[str]:
        return cast(Optional[str], self.data['parent_qty_pref_units'])

    @property
    def nutrient_mass_g(self) -> Optional[float]:
        return cast(Optional[float], self.data['nutrient_mass_g'])
                        
    @property
    def nutrient_mass_pref_units(self) -> Optional[str]:
        return cast(Optional[str], self.data['nutrient_mass_pref_units'])

    @property
    def percentage(self) -> Optional[float]:
        # Catch if I am undefined;
        if not self.defined:
            return None

        return (self.nutrient_mass_g/self.parent_mass_g)*100