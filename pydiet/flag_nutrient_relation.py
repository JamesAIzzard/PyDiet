class FlagNutrientRelation:
    def __init__(self, flag_name: str, nutrient_name: str, implies_has_nutrient: bool):
        self.flag_name = flag_name
        self.nutrient_name = nutrient_name
        self.implies_has_nutrient = implies_has_nutrient

    def asserts_has_no_nutrient(self) -> bool:
        """Returns True/False to indicate if the flag asserts the nutrient qty is zero."""
        return not self.implies_has_nutrient
