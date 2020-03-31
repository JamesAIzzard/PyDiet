from pathlib import Path
from typing import Dict, List


def cwd() -> str:
    return str(Path.cwd())


INGREDIENT_DATAFILE_TEMPLATE_NAME = 'template'
INGREDIENT_DB_PATH = cwd()+'/pydiet/database/ingredients/'
MANDATORY_NUTRIENTS:List[str] = []  # TODO - Fill these in!
NUTRIENT_ALIASES: Dict[str, List[str]] = {
    "aspartic_acid": ["aspartate"],
    "glutamic_acid": ["glutamate"],
    "butyric_acid": ["C4"],
    "caproic_acid": ["C6"],
    "caprylic_acid": ["C8"],
    "capric_acid": ["C10"],
    "lauric_acid": ["C12"],
    "myristic_acid": ["C14"],
    "pentadecanoic_acid": ["C15"],
    "palmitic_acid" : ["C16"],
    "margaric_acid" : ["C17"],
    "stearic_acid" : ["C18"],
    "arachidic_acid" : ["C20"],
    "behenic_acid" : ["C22"],
    "lignoceric_acid" : ["C24"],
    "cerotic_acid" : ["C26"],
    "linoleic_acid" : ["LA"],
    "a_linolenic_acid" : ["alpha_linolenic_acid", "ALA"],
    "stearidonic_acid" : ["SDA"],
    "arachidonic_acid" : ["ETA"],
    "timnodonic_acid" : ["EPA", "eicosapentaenoic_acid"],
    "clupanodonic_acid" : ["DPA"],
    "cervonic_acid" : ["DHA"],
    "thiamin" : ["vitamin_b1"],
    "riboflavin" : ["vitamin_b2"],
    "niacin" : ["vitamin_b3"],
    "pantothenic_acid" : ["vitamin_b5"],
    "biotin" : ["vitamin_b7"],
    "folate" : ["vitamin_b9"]
}
NUTRIENT_GROUP_DEFINITIONS:Dict[str, List[str]] = {
    "vitamin_b6" : [
        "pyridoxine",
        "pyridoxal-5-phosphate",
        "pyridoxamine"
    ]
}
