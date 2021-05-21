"""Converter for old ingredient data format to new ingredient data format."""
import json

import model
import persistence
import tests

ingredient_db_filepath = f"{persistence.configs.path_into_db}/ingredients"
index_filepath = f"{ingredient_db_filepath}/index.json"

# Pull in the index file;
with open(index_filepath, 'r') as fh:
    raw_data = fh.read()
    index = json.loads(raw_data)

# Cycle through each ingredient in the index;
for df_name, unique_name in index.items():
    print(f"Converting {unique_name} / {df_name}")

    # Load the data up;
    # noinspection PyProtectedMember
    old_data = persistence.main._read_datafile(f"{ingredient_db_filepath}/{df_name}.json")

    # Build the new nutrient_ratios_data dict;
    nutrient_ratios_data = {}
    for nutr_name, nr_data in old_data['nutrients'].items():
        if nr_data['nutrient_g_per_subject_g'] is not None:
            nutrient_ratios_data[nutr_name] = model.nutrients.NutrientRatioData(
                nutrient_mass_data=model.quantity.QuantityData(
                    quantity_in_g=nr_data['nutrient_g_per_subject_g'],
                    pref_unit=nr_data['nutrient_pref_units']
                ),
                subject_ref_qty_data=model.quantity.QuantityData(
                    quantity_in_g=100,
                    pref_unit='g'
                )
            )

    # Build the new flag_data dict;
    flag_data = {
        'nut_free': old_data['flag_data']['nut_free'],
        'vegan': old_data['flag_data']['vegan'],
        'vegetarian': old_data['flag_data']['vegetarian']
    }

    # Create the new data dict;
    new_data = model.ingredients.IngredientData(
        cost_per_qty_data=model.cost.CostPerQtyData(
            quantity_in_g=100,
            pref_unit='g',
            cost_per_g=old_data['cost_per_qty_data']
        ),
        flag_data=flag_data,
        name=old_data['name'],
        nutrient_ratios_data=nutrient_ratios_data,
        extended_units_data=model.quantity.ExtendedUnitsData(
            g_per_ml=old_data['bulk']['g_per_ml'],
            piece_mass_g=old_data['bulk']['piece_mass_g']
        )
    )

    # Deal with the old bulk data conversion

    with open(f"{ingredient_db_filepath}/{df_name}.json", 'w') as fh:
        json.dump(new_data, fh, indent=2, sort_keys=True)

