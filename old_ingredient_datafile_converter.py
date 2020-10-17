import json

from pydiet import ingredients, nutrients, quantity, persistence

route_into_old_df_dir = "C:/Users/James Izzard/Downloads/ingredients/"
old_index_filepath = route_into_old_df_dir + 'index.json'

# Read the old index;
with open(old_index_filepath, 'r') as fh:
    raw_data = fh.read()
    old_index = json.loads(raw_data)

for df_name in old_index:
    # Load the original data;
    with open(route_into_old_df_dir + df_name + '.json') as fh:
        raw_data = fh.read()
        old_data = json.loads(raw_data)

    i = ingredients.ingredient_service.load_new_ingredient()

    # Port the name across;
    i.set_name(old_data['name'])

    # Port the bulk data across;
    if None not in old_data['vol_density'].values():
        i.set_density(
            old_data['vol_density']['ingredient_mass'],
            old_data['vol_density']['ingredient_mass_units'],
            old_data['vol_density']['ingredient_vol'],
            old_data['vol_density']['ingredient_vol_units']
        )

    # Port the cost across;
    cost_gbp = old_data['cost_per_mass']['cost']
    qty = old_data['cost_per_mass']['ingredient_qty']
    unit = old_data['cost_per_mass']['ingredient_qty_units']
    i.set_cost(cost_gbp, qty, unit)

    # Port the flags across;
    for flag_name in old_data['flags']:
        i.set_flag(flag_name, old_data['flags'][flag_name])

    # Port the nutrients across;
    for nutrient_name in old_data['nutrients']:
        if None in old_data['nutrients'][nutrient_name].values():
            continue
        ingredient_qty_g = quantity.services.convert_qty_unit(
            qty=old_data['nutrients'][nutrient_name]['ingredient_qty'],
            start_unit=old_data['nutrients'][nutrient_name]['ingredient_qty_units'],
            end_unit='g',
            g_per_ml=i.g_per_ml
        )
        nutrient_qty_g = quantity.services.convert_qty_unit(
            qty=old_data['nutrients'][nutrient_name]['nutrient_mass'],
            start_unit=old_data['nutrients'][nutrient_name]['nutrient_mass_units'],
            end_unit='g'
        )
        nutrient_data = nutrients.supports_nutrient_content.NutrientData(
            nutrient_g_per_subject_g=nutrient_qty_g / ingredient_qty_g,
            nutrient_pref_units=old_data['nutrients'][nutrient_name]['nutrient_mass_units']
        )
        i.set_nutrient_data(nutrient_name, nutrient_data)

    i._datafile_name = None

    persistence.persistence_service.save(i)
