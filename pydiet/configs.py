from pathlib import Path
from typing import Dict, List


def cwd() -> str:
    return str(Path.cwd())

INGREDIENT_DATAFILE_TEMPLATE_NAME = 'template'
RECIPE_DATAFILE_TEMPLATE_NAME = 'template'
INGREDIENT_INDEX_NAME = 'index'
RECIPE_INDEX_NAME = 'index'
DAY_GOALS_INDEX_NAME = 'index'
INGREDIENT_DB_PATH = cwd()+'/pydiet/database/ingredients/'
RECIPE_DB_PATH = cwd()+'/pydiet/database/recipes/'
DAY_GOALS_DB_PATH = cwd()+'/pydiet/database/goals/day_goals/'
PRIMARY_NUTRIENTS: List[str] = [
    "carbohydrate",
    "fat",
    "saturated_fat",
    "monounsaturated_fat",
    "polyunsaturated_fat",
    "protein",
    "sodium"
]
NUTRIENT_ALIASES: Dict[str, List[str]] = {
    "a_carotene": ["alpha_carotene"],
    "a_linolenic_acid": ["alpha_linolenic_acid", "ALA"],
    "amylose": ["starch"],
    "arachidic_acid": ["C20"],
    "arachidonic_acid": ["ETA"],
    "aspartic_acid": ["aspartate"],
    "b_carotene": ["beta_carotene"],
    "behenic_acid": ["C22", "docosanoic_acid"],
    "biotin": ["vitamin_b7"],
    "butyric_acid": ["C4"],
    "capric_acid": ["C10"],
    "caproic_acid": ["C6"],
    "caprylic_acid": ["C8"],
    "cerotic_acid": ["C26"],
    "cervonic_acid": ["DHA"],
    "clupanodonic_acid": ["DPA"],
    "cobalamin": ["vitamin_b12"],
    "folate": ["vitamin_b9"],
    "glutamic_acid": ["glutamate"],
    "lauric_acid": ["C12"],
    "lignoceric_acid": ["C24"],
    "linoleic_acid": ["LA"],
    "margaric_acid": ["C17"],
    "myristic_acid": ["C14"],
    "niacin": ["vitamin_b3"],
    "palmitic_acid": ["C16"],
    "pantothenic_acid": ["vitamin_b5"],
    "pentadecanoic_acid": ["C15"],
    "riboflavin": ["vitamin_b2"],
    "stearic_acid": ["C18"],
    "stearidonic_acid": ["SDA"],
    "thiamin": ["vitamin_b1"],
    "timnodonic_acid": ["EPA", "eicosapentaenoic_acid"],
    "vitamin_c": ["ascorbic_acid"],
    "vitamin_k1": ["phylloquinone"],
    "vitamin_k2": ["menaquinone"],
}
NUTRIENT_GROUP_DEFINITIONS: Dict[str, List[str]] = {
    "carbohydrate": ["glucose", "sucrose", "ribose", "amylose", "amylopectin", "maltose", "galactose", "fructose", "lactose"],
    "cartenoids": ["a_carotene", "b_carotene", "cryptoxanthin", "lutein", "lycopene", "zeaxanthin"],
    "fat": ["monounsaturated_fat", "polyunsaturated_fat", "saturated_fat", "trans_fats"],
    "fibre": [],
    "monounsaturated_fat": ["myristol", "pentadecenoic", "palmitoyl", "heptadecenoic", "oleic_acid", "eicosen", "erucic_acid", "nervonic_acid"],
    "omega_3": [],
    "omega_6": [],
    "polyunsaturated_fat": [],
    "protein": ["alanine", "arginine", "aspartic_acid", "asparagine", "cysteine", "glutamic_acid", "glutamine", "glycine", "histidine", "isoleucine", "leucine", "lysine", "methionine", "phenylalanine", "proline", "serine", "threonine", "tryptophan", "tyrosine", "valine"],
    "saturated_fat": [],
    "trans_fats": [],
    "vitamin_a": ["retinol", "retinal", "retinoic_acid", "b_carotene"],
    "vitamin_b6": ["pyridoxine", "pyridoxal_5_phosphate", "pyridoxamine"],
    "vitamin_d": ["ergocalciferol", "cholecalciferol"],
    "vitamin_e": [],
    "vitamin_k": ["vitamin_k1", "vitamin_k2"],
}
NUTRIENT_FLAG_RELS: Dict[str, List[str]] = {
    "alcohol_free": ["alcohol"]
}

PRESET_SERVE_TIMES: Dict[str, str] = {
    "Breakfast": "04:00-10:00",
    "Lunch": "12:00-15:00",
    "Dinner": "17:00-22:00",
    "Any Time": "00:00-23:59"
}

RECIPE_TAGS: List[str] = [
    "main",
    "side",
    "sweet",
    "savory",
    "snack",
    "drink"
]
