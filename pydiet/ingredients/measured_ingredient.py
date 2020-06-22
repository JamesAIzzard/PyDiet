class MeasuredIngredient():
    def __init__(self, ingredient):
        self._ingredient = ingredient
        self._quantity: float
        self._quantity_units: str

    @property
    def calories(self)-> float:
        # Returns calorie total for this amount
        # of ingredinet.
        raise NotImplementedError
    
    def nutrient_mass(self, nutrient_name:str) -> float:
        # Returns the mass of the specified nutrient for
        # this amount of the ingredient.
        raise NotImplementedError 