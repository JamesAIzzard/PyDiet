from typing import Protocol

from pydiet import nutrients, quantity


class SupportsNutrientQuantities(nutrients.supports_nutritional_profile.SupportsNutritionalProfile,
                                 quantity.supports_quantity.SupportsQuantity,
                                 Protocol):
    
    def get_nutrient_mass_g(self, nutrient_name:str) -> float:
        return self.quantity_g * self.get_readonly_nutrient_data(nutrient_name)
