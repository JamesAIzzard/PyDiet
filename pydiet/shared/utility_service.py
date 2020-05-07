from typing import Tuple, List, Dict, TYPE_CHECKING
from difflib import SequenceMatcher

from pinjector import inject

from pydiet.shared.exceptions import UnknownUnitError

if TYPE_CHECKING:
    from pydiet.data import repository_service

_G_CONVERSIONS = {
    "ug": 1e-6,  # 1 microgram = 0.000001 grams
    "mg": 1e-3,  # 1 milligram = 0.001 grams
    "g": 1,  # 1 gram = 1 gram! :)
    "kg": 1e3,  # 1 kilogram = 1000 grams
}

_ML_CONVERSIONS = {
    "ml": 1,
    "cm3": 1,    
    "l": 1e3, # 1L = 1000 ml
    "m3": 1e6,    
    "quart": 946.4,
    "tsp": 4.929,
    "tbsp": 14.79
}

def recognised_mass_units()->List[str]:
    return list(_G_CONVERSIONS.keys())

def recognised_vol_units()->List[str]:
    return list(_ML_CONVERSIONS.keys())

def recognised_qty_units()->List[str]:
    return recognised_mass_units() + \
        recognised_vol_units()

def validate_unit(unit:str)->None:
    if not unit in _G_CONVERSIONS.keys() and \
        not unit in _ML_CONVERSIONS.keys():
        raise UnknownUnitError()

def convert_mass(mass: float, start_units: str, end_units: str) -> float:
    # Lowercase all units;
    start_units = start_units.lower()
    end_units = end_units.lower()
    # Convert value to grams first
    mass_in_g = _G_CONVERSIONS[start_units]*mass
    return mass_in_g/_G_CONVERSIONS[end_units]

def convert_volume(volume: float, start_units:str, end_units: str) -> float:
    # Lowercase all units;
    start_units = start_units.lower()
    end_units = end_units.lower()    
    vol_in_ml = _ML_CONVERSIONS[start_units]*volume
    return vol_in_ml/_ML_CONVERSIONS[end_units]

def convert_vol_to_grams(
    volume:float, 
    vol_units:str, 
    density_g_per_ml:float
)->float:
    # Lowercase units;
    vol_units = vol_units.lower()
    # First convert the volume to ml;
    vol_ml = convert_volume(volume, vol_units, 'ml')
    # Calculate mass in g;
    mass_g = density_g_per_ml*vol_ml
    # Return result;
    return mass_g

def get_all_nutrient_names()->List[str]:
    rp:'repository_service' = inject('pydiet.repository_service')
    data_template = rp.read_ingredient_template_data()
    return list(data_template['nutrients'].keys())

def sentence_case(text: str) -> str:
    '''Capitalizes the first letter of each word in the
    text provided.

    Args:
        text (str): Text to convert to sentence case.

    Returns:
        str: Text with sentence case capitalisation.
    '''
    words_list = text.split('_')
    for word in words_list:
        word.capitalize()
    return ' '.join(words_list)

def parse_number_and_units(mass_and_units: str) -> Tuple[float, str]:
    output = None
    # Strip any initial whitespace;
    mass_and_units = mass_and_units.replace(' ', '')
    # Work along the string until you find something which is
    # not a number;
    for i, char in enumerate(mass_and_units):
        # If char cannot be parsed as a number,
        # split the string here;
        if not char.isnumeric() and not char == '.':
            mass_part = float(mass_and_units[:i])
            units_part = str(mass_and_units[i:])
            output = (mass_part, units_part)
            break
    if not output:
        raise ValueError('Unable to parse {} into a mass and unit.'
                            .format(mass_and_units))
    # Return tuple;
    return output

def score_similarity(words:List[str], search_term:str)->Dict[str, float]:
    scores = {}
    for word in words:
        scores[word] = SequenceMatcher(None, search_term, word).ratio()
    return scores
