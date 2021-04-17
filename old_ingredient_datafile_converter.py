import model
import persistence
import json

index = persistence._read_index(cls=model.ingredients.Ingredient)
flags_to_mod = [
    ("alcohol_free", "alcohol"),
    ("caffiene_free", "caffiene"),
    ("lactose_free", "lactose"),
    ("gluten_free", "gluten")
]
for df_name, unique_name in index.items():
    print(df_name, unique_name)
    data = persistence._read_datafile(model.ingredients.Ingredient.get_path_into_db() + df_name + '.json')
    for flag_bundle in flags_to_mod:
        flag_name = flag_bundle[0]
        nutrient_name = flag_bundle[1]
        if nutrient_name not in data["nutrients"].keys():
            data["nutrients"][nutrient_name] = {
                "nutrient_g_per_subject_g": None,
                "nutrient_pref_units": "g"
            }
        if data["flags"][flag_name] is True:
            data["nutrients"][nutrient_name]["nutrient_g_per_subject_g"] = 0
        elif data["flags"][flag_name] is False:
            data["nutrients"][nutrient_name]["nutrient_g_per_subject_g"] = None
        del data["flags"][flag_name]
    with open(model.ingredients.Ingredient.get_path_into_db() + df_name + '.json', 'w') as fh:
        json.dump(data, fh, indent=2, sort_keys=True)

