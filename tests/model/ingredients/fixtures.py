"""Fixtures for ingredient module testing."""

INGREDIENT_NAME_WITH = {
    "name_raspberry": "Raspberry",
    "properly_defined": "Raspberry",
    "density_defined": "Lemon Juice",
    "density_undefined": "Aubergine",
    "piece_mass_defined": "Aubergine",
    "piece_mass_undefined": "Lemon Juice",
    "cost_per_g_defined": "Aubergine",
    "cost_per_g_undefined": "Courgette",
    "flag_dofs_all_defined": "Spinach",
    "flag_dofs_two_undefined": "Lemon",
    "nutrient_ratios_protein_defined": "Smoked Salmon",
    "nutrient_ratios_iron_undefined": "Smoked Salmon",
    "nutrient_ratios_8_ratios_defined": "Red Pepper",
}


def get_ingredient_name_with(characteristic: str) -> str:
    """Returns an ingredient name matching the specified characteristic.
    Performs a lookup on the table above.
    """
    return INGREDIENT_NAME_WITH[characteristic]
