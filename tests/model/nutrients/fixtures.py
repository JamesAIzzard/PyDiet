import model


def get_protein() -> 'model.nutrients.Nutrient':
    return model.nutrients.Nutrient('protein')


def get_undefined_protein_mass() -> 'model.nutrients.NutrientMass':
    return model.nutrients.NutrientMass(nutrient=get_protein())


def get_32g_protein() -> 'model.nutrients.NutrientMass':
    return model.nutrients.NutrientMass(
        nutrient=get_protein(),
        nutrient_mass_data=model.nutrients.NutrientMassData(
            bulk_data=model.quantity.BulkData(
                pref_unit='g',
                ref_qty=100,
                g_per_ml=None,
                piece_mass_g=None
            ),
            quantity_in_g=32
        )
    )


def get_undefined_settable_protein_mass() -> 'model.nutrients.SettableNutrientMass':
    return model.nutrients.SettableNutrientMass(nutrient=get_protein())
