import copy
from typing import List, Dict

from . import configs, exceptions, validation, main
from .main import (
    get_nutrient_primary_name,
    get_nutrient_alias_names,
    get_calories_per_g,
    nutrient_ratio_data_is_defined,
    validate_nutrient_family_masses,
    get_n_closest_nutrient_names
)
from .nutrient import Nutrient
from .nutrient_mass import (
    NutrientMass,
    SettableNutrientMass,
    NutrientMassData
)
from .nutrient_ratios import (
    NutrientRatioData,
    NutrientRatio,
    SettableNutrientRatio,
    NutrientRatiosData,
    HasNutrientRatios,
    HasSettableNutrientRatios
)


def build_nutrient_group_name_list(nutrient_configs: 'configs') -> List[str]:
    """Returns a list of all nutrient names, based on the information in the config file."""
    return list(nutrient_configs.NUTRIENT_GROUP_DEFINITIONS.keys())


def build_optional_nutrient_name_list(nutrient_configs: 'configs') -> List[str]:
    """Returns a list of all optional nutrient names, based on the information in the config file."""
    return list(set(nutrient_configs.ALL_PRIMARY_NUTRIENT_NAMES).difference(
        set(nutrient_configs.MANDATORY_NUTRIENT_NAMES)))


def build_primary_and_alias_nutrient_names(nutrient_configs: 'configs') -> List[str]:
    """Returns a list of all primary and alias names known to the system, derived from the config file."""
    primary_and_alias_nutrient_names = copy.copy(nutrient_configs.ALL_PRIMARY_NUTRIENT_NAMES)
    for primary_name, aliases in nutrient_configs.NUTRIENT_ALIASES.items():
        primary_and_alias_nutrient_names += aliases
    return primary_and_alias_nutrient_names


def build_global_nutrient_list(nutrient_configs: 'configs') -> Dict[str, 'Nutrient']:
    """Constructs the nutrient tree and returns it."""
    # Create the global list to store nutrients. This is ultimately what we will return;
    global_nutrients: Dict[str, 'Nutrient'] = {}

    # Work through the list of primary names and init an instance for each;
    for primary_nutrient_name in nutrient_configs.ALL_PRIMARY_NUTRIENT_NAMES:
        # First, collect up all the names we will need;
        # Start with the alias names;
        if primary_nutrient_name in nutrient_configs.NUTRIENT_ALIASES.keys():
            alias_names = nutrient_configs.NUTRIENT_ALIASES[primary_nutrient_name]
        else:
            alias_names = []

        # Now grab any calorie data;
        if primary_nutrient_name in nutrient_configs.CALORIE_NUTRIENTS.keys():
            calories_per_g = nutrient_configs.CALORIE_NUTRIENTS[primary_nutrient_name]
        else:
            calories_per_g = 0

        # Now instantiate the nutrient;
        global_nutrients[primary_nutrient_name] = Nutrient(
            nutrient_name=primary_nutrient_name,
            alias_names=alias_names,
            calories_per_g=calories_per_g,
            direct_child_nutrient_names=_gather_direct_child_names(primary_nutrient_name, nutrient_configs),
            direct_parent_nutrient_names=_gather_direct_parent_names(primary_nutrient_name, nutrient_configs),
            all_sibling_nutrient_names=_gather_direct_sibling_names(primary_nutrient_name, nutrient_configs),
            all_descendant_nutrient_names=_gather_descendant_names(primary_nutrient_name, nutrient_configs),
            all_ascendant_nutrient_names=_gather_ascendant_names(primary_nutrient_name, nutrient_configs),
            all_relative_nutrient_names=_gather_all_relative_names(primary_nutrient_name, nutrient_configs),
            global_nutrients=global_nutrients
        )

    # Return the completed list;
    return global_nutrients


def _gather_descendant_names(primary_nutr_name: str, nutrient_configs: 'configs') -> List[str]:
    """Returns a dictionary of all descendants of the named nutrient."""

    # Create a list to store the descendants, and another to add to during looping through descendents
    # which have already been collected, (we can't change the size of a list while iterating through it);
    descendants: List[str] = []
    to_add: List[str] = []

    # OK, so if this nutrient is a group definition, then we know it has descendants;
    if primary_nutr_name in nutrient_configs.NUTRIENT_GROUP_DEFINITIONS.keys():
        descendants += nutrient_configs.NUTRIENT_GROUP_DEFINITIONS[primary_nutr_name]

    # Now, work through the list of descendants you just collected, and for each one of those,
    # gather their descendants, but add them to the holding list, so you don't change the descendants
    # list mid-loop;
    for child_nutrient in descendants:
        to_add += _gather_descendant_names(child_nutrient, nutrient_configs)
    # Update the descendants list, with the newfound desecedants;
    descendants += to_add
    # and return everything;
    return descendants


def _gather_ascendant_names(primary_nutr_name: str, nutrient_configs: 'configs') -> List[str]:
    """Returns a list of all ascendants of the named nutrient."""
    # Create a list to store the ascendants, and another to add to during looping through descendents
    # which have already been collected, (we can't change the size of a list while iterating through it);
    ascendants: List[str] = []
    to_add: List[str] = []

    # First, check if this nutrient name is in a group;
    for group_name, group_member_names in nutrient_configs.NUTRIENT_GROUP_DEFINITIONS.items():
        # If it is, add the group name to the ascendants list;
        if primary_nutr_name in group_member_names:
            ascendants.append(group_name)

    # Now loop through the ascendants list;
    for ascendant in ascendants:
        # and collect their ascendants in the holding list;
        to_add += _gather_ascendant_names(ascendant, nutrient_configs)

    # Finally, update the ascendants list with the holding list, and return everything;
    ascendants += to_add
    return ascendants


def _gather_direct_sibling_names(primary_nutr_name: str, nutrient_configs: 'configs') -> List[str]:
    """Returns a dictionary of all direct siblings to the named nutrient."""
    # Dict to hold results;
    siblings: List[str] = []
    # Cycle through every defined group;
    for group_name, group_member_names in nutrient_configs.NUTRIENT_GROUP_DEFINITIONS.items():
        # If we find this nutrient in the group;
        if primary_nutr_name in group_member_names:
            # then add every member of the group to the siblings list;
            for group_member_name in group_member_names:
                # but don't add the main nutrient to its own list of siblings!;
                if group_member_name is not primary_nutr_name:
                    siblings.append(group_member_name)
    # Return everything;
    return siblings


def _gather_direct_parent_names(primary_nutr_name: str, nutrient_configs: 'configs') -> List[str]:
    """Returns a dictionary of parent nutrients to the specified nutrient."""
    # Create a dictionary to hold parents;
    parents: List[str] = []
    # Cycle through the group defininion list;
    for group_name, group_member_names in nutrient_configs.NUTRIENT_GROUP_DEFINITIONS.items():
        # If we find this nutrient in the group, then we know the group is a parent;
        if primary_nutr_name in group_member_names:
            parents.append(group_name)
    # All done, return everything;
    return parents


def _gather_direct_child_names(primary_nutr_name: str, nutrient_configs: 'configs') -> List[str]:
    """Returns a list of nutrient names which are direct children to the named nutrient."""
    # Dict to collect children;
    children: List[str] = []
    # If this nutrient has children;
    if primary_nutr_name in nutrient_configs.NUTRIENT_GROUP_DEFINITIONS.keys():
        children += (nutrient_configs.NUTRIENT_GROUP_DEFINITIONS[primary_nutr_name])
    # Return everything;
    return children


def _gather_all_relative_names(primary_nutr_name: str,
                               nutrient_configs: 'configs',
                               checked: List[str] = None) -> List[str]:
    """Returns a dictionary of all relative nutrients to the named nutrient."""
    # Create a nutrient checklist to track which ones have been crawled in the tree. This prevents
    # infinite recursion;
    if checked is None:
        checked = []

    # Create list to store relatives, and temp list to append to while looping through relatives;
    relatives: List[str] = []
    to_add: List[str] = []

    # Gather the nutrients across, up and down from this nutrient;
    relatives += _gather_direct_sibling_names(primary_nutr_name, nutrient_configs)
    relatives += _gather_ascendant_names(primary_nutr_name, nutrient_configs)
    relatives += _gather_descendant_names(primary_nutr_name, nutrient_configs)

    # Add this nutrient to the checklist;
    checked.append(primary_nutr_name)

    # Now cycle through all nutrients which have not been checked yet;
    for relative in relatives:
        if relative not in checked:
            to_add += _gather_all_relative_names(relative, nutrient_configs, checked)

    # Update the main list;
    relatives += to_add

    # Remove any duplicates;
    relatives = list(set(relatives))

    # Remove myself from the list;
    if primary_nutr_name in relatives:
        relatives.remove(primary_nutr_name)

    # Return everything;
    return relatives


# Create the derived name lists, ready for initialisation;
PRIMARY_AND_ALIAS_NUTRIENT_NAMES: List[str] = build_primary_and_alias_nutrient_names(configs)
NUTRIENT_GROUP_NAMES: List[str] = build_nutrient_group_name_list(configs)
OPTIONAL_NUTRIENT_NAMES: List[str] = build_optional_nutrient_name_list(configs)

# Now build the global nutrient list;
GLOBAL_NUTRIENTS = build_global_nutrient_list(configs)

# Check the configs are OK;
validation.validate_configs(configs)
