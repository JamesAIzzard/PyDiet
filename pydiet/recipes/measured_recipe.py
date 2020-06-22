class MeasuredRecipe():
    def __init__(self, recipe):
        self._recipe = recipe
        self._measured_ingredients = {}

    @property
    def calories(self) -> float:
        # Returns the total number of calories in the set
        # of ingredients constituting this recipe.
        raise NotImplementedError

    def nutrient_mass(self, nutrient_name:str) -> float:
        # Returns the total mass of the specified nutrient for
        # the ingredients constituting this recipe. 
        raise NotImplementedError