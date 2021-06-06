"""Converter for old ingredient data format to new ingredient data format."""
import copy
import json

import model.quantity
import persistence
# from tests.persistence.configs import path_into_db as path_into_db
from persistence.configs import path_into_db as path_into_db

ingredient_db_filepath = f"{path_into_db}/ingredients"
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

    # Create a copy which we will update;
    updated_data = copy.deepcopy(old_data)

    # Make the change to the data;
    for nutrient_name in old_data['nutrient_ratios_data'].keys():
        # Update the new data;
        updated_data['nutrient_ratios_data'][nutrient_name] = model.quantity.QuantityRatioData(
            subject_qty_data=model.quantity.QuantityData(
                quantity_in_g=old_data['nutrient_ratios_data'][nutrient_name]['nutrient_mass_data']['quantity_in_g'],
                pref_unit=old_data['nutrient_ratios_data'][nutrient_name]['nutrient_mass_data']['pref_unit'],
            ),
            host_qty_data=model.quantity.QuantityData(
                quantity_in_g=old_data['nutrient_ratios_data'][nutrient_name]['subject_ref_qty_data']['quantity_in_g'],
                pref_unit=old_data['nutrient_ratios_data'][nutrient_name]['subject_ref_qty_data']['pref_unit'],
            )
        )

    # Overwrite the old data with its updated version;
    with open(f"{ingredient_db_filepath}/{df_name}.json", 'w') as fh:
        json.dump(updated_data, fh, indent=2, sort_keys=True)
