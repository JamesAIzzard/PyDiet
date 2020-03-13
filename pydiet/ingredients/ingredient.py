from typing import TYPE_CHECKING, Union, Dict
from pydiet.injector import injector
if TYPE_CHECKING:
    from pydiet.utility_service import UtilityService


class Ingredient():
    def __init__(self, data):
        self._data = data
        self._utility_service: 'UtilityService' = injector.utility_service

    @property
    def macronutrient_data(self)->Dict:
        return self._data['macronutrients']

    @property
    def macronutrient_totals_data(self)->Dict:
        return self._data['macronutrient_totals']

    @property
    def micronutrient_data(self)->Dict:
        return self._data['micronutrients']

    @property
    def all_nutrients_data(self)->Dict:
        all_nutrient_data = {}
        all_nutrient_data.update(self.macronutrient_data)
        all_nutrient_data.update(self.micronutrient_data)
        return all_nutrient_data
    
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
                self._data['cost_per_mass']['mass'],
                self._data['cost_per_mass']['mass_units'], "g"
            )
            return self._data['cost_per_mass']['cost']/conversion_factor
        else:
            return None

    @property
    def cost_data(self)-> Union[Dict, None]:
        return self._data['cost_per_mass']

    @property
    def total_carbohydrate_data(self)->Dict:
        return self._data['total_carbohydrate']

    @property
    def total_carbohydrate_percentage(self)->Union[float, None]:
        return self.get_nutrient_percentage('total_carbohydrate')

    @property
    def total_fat_data(self)->Dict:
        return self._data['total_fat']

    @property
    def total_fat_percentage(self)->Union[float, None]:
        return self.get_nutrient_percentage('total_fat')

    def set_cost(self, cost: float, mass: float, mass_units: str) -> None:
        self._data['cost_per_mass']['cost'] = cost
        self._data['cost_per_mass']['mass'] = mass
        self._data['cost_per_mass']['mass_units'] = mass_units

    def check_nutrient_is_defined(self, nutrient_name: str) -> bool:
        nutrient_data = self.all_nutrients_data[nutrient_name]
        # Iterate through the fields and return false if one isn't
        # defined;
        for field in nutrient_data.keys():
            if not nutrient_data[field]:
                return False
        return True # If there were no undefined fields.

    def get_flag(self, flag_name:str)->Union[bool, None]:
        return self._data['flags'][flag_name]

    def get_nutrient_data(self, nutrient_name:str)->Union[Dict, None]:
        nutrients_data = self.all_nutrients_data
        if nutrient_name in nutrients_data.keys():
            return nutrients_data[nutrient_name]

    def get_nutrient_percentage(self, nutrient_name:str)->Union[float, None]:
        if self.check_nutrient_is_defined(nutrient_name):
            nutrient_data = self.get_nutrient_data(nutrient_name)
            nutrient_mass_in_grams = injector.utility_service.convert_mass(
                nutrient_data['mass'], nutrient_data['mass_units'], 'g'
            )
            sample_mass_in_grams = injector.utility_service.convert_mass(
                nutrient_data['mass_per'], nutrient_data['mass_per_units'], 'g'
            )
            return (nutrient_mass_in_grams/sample_mass_in_grams)*100
