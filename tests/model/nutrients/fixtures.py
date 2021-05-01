import model


def get_protein() -> 'model.nutrients.Nutrient':
    return model.nutrients.Nutrient('protein')


def get_vitamin_b12() -> 'model.nutrients.Nutrient':
    return model.nutrients.Nutrient('vitamin_b12')


def get_undefined_protein_mass() -> 'model.nutrients.NutrientMass':
    return model.nutrients.NutrientMass(
        nutrient=get_protein(),
        get_quantity_in_g=lambda: None,
        get_quantity_pref_unit='g'
    )


def get_32g_protein() -> 'model.nutrients.NutrientMass':
    return model.nutrients.NutrientMass(
        nutrient=get_protein(),
        get_quantity_in_g=lambda: 32,
        get_quantity_pref_unit='g'
    )


def get_undefined_settable_protein_mass() -> 'model.nutrients.SettableNutrientMass':
    return model.nutrients.SettableNutrientMass(nutrient=get_protein())
