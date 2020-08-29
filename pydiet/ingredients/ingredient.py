import copy
from pydiet.nutrients import nutrients_service
from typing import Optional, Dict, List, TypedDict, TYPE_CHECKING

from pydiet import nutrients, defining, quantity, cost, flags, quantity

if TYPE_CHECKING:
    from pydiet.cost.supports_cost import CostData
    from pydiet.quantity.supports_density import DensityData
    from pydiet.quantity.supports_unit_mass import UnitMassData
    from pydiet.nutrients.supports_nutritional_composition import NutrientCompositionData


class IngredientData(TypedDict):
    cost: 'CostData'
    flags: Dict[str, Optional[bool]]
    name: Optional[str]
    nutrients: Dict[str, 'NutrientCompositionData']
    density: 'DensityData'
    unit_mass: 'UnitMassData'

ingredient_data_template = {
    "cost": {},
    "flags": {},
    "name": None,
    "nutrients": {},
    "density": {},
    "unit_mass": {}
}


class Ingredient(defining.supports_definition.SupportsDefinition,
                 cost.supports_cost.SupportsCostSetting,
                 flags.supports_flags.SupportsFlagSetting,
                 nutrients.supports_nutritional_composition.SupportsNutritionalCompositionSetting,
                 quantity.supports_density.SupportsDensitySetting,
                 quantity.supports_unit_mass.SupportsUnitMass):

    def __init__(self, data: IngredientData):
        self._data = data

    @property
    def name(self) -> Optional[str]:
        return self._data['name']

    @name.setter
    def name(self, value: str) -> None:
        self._data['name'] = value

    @property
    def missing_mandatory_attrs(self) -> List[str]:
        attr_names = []
        # Check name;
        if self.name == None:
            attr_names.append('name')
        # Check flags;
        # Check nutrients;
        # Check density;
        return attr_names

    @property
    def readonly_cost_data(self) -> 'CostData':
        return copy.deepcopy(self.cost_data)

    @property
    def cost_data(self) -> 'CostData':
        return self._data['cost']

    @property
    def flag_data(self) -> Dict[str, Optional[bool]]:
        return self._data['flags']

    @property
    def readonly_flag_data(self) -> Dict[str, Optional[bool]]:
        return copy.deepcopy(self.flag_data)

    @property
    def nutritional_composition_data(self) -> Dict[str, 'NutrientCompositionData']:
        return self._data['nutrients']

    @property
    def readonly_nutritional_composition_data(self) -> Dict[str, 'NutrientCompositionData']:
        return copy.deepcopy(self.nutritional_composition_data) 

    @property
    def readonly_density_data(self) -> 'DensityData':
        raise NotImplementedError        


