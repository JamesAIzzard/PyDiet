from typing import List, Dict

import model
# Bring the next couple of modules in as relative, because they are required during initialisation;
from . import configs, main


def _check_init_and_return(nutrient_name: str) -> 'Nutrient':
    """Helper function to check the nutrient has been initialised on the global list.
    If it hasn't been initialised yet, this is done. Either way, a reference to the instance,
    is returned."""
    if nutrient_name not in main.GLOBAL_NUTRIENTS.keys():
        main.GLOBAL_NUTRIENTS[nutrient_name] = Nutrient(nutrient_name)
    return main.GLOBAL_NUTRIENTS[nutrient_name]


def _gather_descendants(nutrient: 'Nutrient') -> Dict[str, 'Nutrient']:
    """Returns a dictionary of all descendants of the named nutrient."""
    # Create a dict to store the descendants, and another to add to during looping through descendents
    # which have already been collected, (we can't change the size of a dict while iterating through it);
    descendants: Dict[str, 'Nutrient'] = {}
    to_add: Dict[str, 'Nutrient'] = {}
    # OK, so if this nutrient is a group definition, then we know it has descendants;
    if nutrient.primary_name in main.NUTRIENT_GROUP_NAMES:
        for child_name in configs.NUTRIENT_GROUP_DEFINITIONS[nutrient.primary_name]:
            # So work through those descendants, and check each one is intialised;
            descendants[child_name] = _check_init_and_return(child_name)
    # Now, work through the list of descendants you just collected, and for each one of those,
    # gather their descendants, but add them to the holding list, so you don't change the descendants
    # list mid-loop;
    for child_nutrient in descendants.values():
        to_add.update(_gather_descendants(child_nutrient))
    # Update the descendants list, with the newfound desecedants;
    descendants.update(to_add)
    # and return everything;
    return descendants


def _gather_ascendants(nutrient: 'Nutrient') -> Dict[str, 'Nutrient']:
    """Returns a dictionary of all ascendants of the named nutrient."""
    # Create two dictionaries, one to colllect ascendants, and another to use to collect more ascendants
    # while recursively looping through the first;
    ascendants: Dict[str, 'Nutrient'] = {}
    to_add: Dict[str, 'Nutrient'] = {}
    # First, check if this nutrient name is in a group;
    for group_name, group_member_names in configs.NUTRIENT_GROUP_DEFINITIONS.items():
        # If it is, add the group name to the ascendants list;
        if nutrient.primary_name in group_member_names:
            ascendants.update({group_name: _check_init_and_return(group_name)})
    # Now loop through the ascendants list;
    for ascendant in ascendants.values():
        # and collect their ascendants in the holding list;
        to_add.update(_gather_ascendants(ascendant))
    # Finally, update the ascendants list with the holding list, and return everything;
    ascendants.update(to_add)
    return ascendants


def _gather_direct_siblings(nutrient: 'Nutrient') -> Dict[str, 'Nutrient']:
    """Returns a dictionary of all direct siblings to the named nutrient."""
    # Dict to hold results;
    siblings: Dict[str, 'Nutrient'] = {}
    # Cycle through every defined group;
    for group_name, group_member_names in configs.NUTRIENT_GROUP_DEFINITIONS.items():
        # If we find this nutrient in the group;
        if nutrient.primary_name in group_member_names:
            # then add every member of the group to the siblings list;
            for group_member_name in group_member_names:
                # but don't add the main nutrient to its own list of siblings!;
                if group_member_name is not nutrient.primary_name:
                    siblings.update({group_member_name: _check_init_and_return(group_member_name)})
    # Return everything;
    return siblings


def _gather_direct_parents(nutrient: 'Nutrient') -> Dict[str, 'Nutrient']:
    """Returns a dictionary of parent nutrients to the specified nutrient."""
    # Create a dictionary to hold parents;
    parents: Dict[str, 'Nutrient'] = {}
    # Cycle through the group defininion list;
    for group_name, group_member_names in configs.NUTRIENT_GROUP_DEFINITIONS.items():
        # If we find this nutrient in the group, then we know the group is a parent;
        if nutrient.primary_name in group_member_names:
            parents.update({group_name: _check_init_and_return(group_name)})
    # All done, return everything;
    return parents


def _gather_direct_children(nutrient: 'Nutrient') -> Dict[str, 'Nutrient']:
    """Returns a dictionary of direct children of the specified nutrient."""
    # Dict to collect children;
    children: Dict[str, 'Nutrient'] = {}
    # If this nutrient has children;
    if nutrient.primary_name in configs.NUTRIENT_GROUP_DEFINITIONS.keys():
        # Cycle through them and add them;
        for child_name in configs.NUTRIENT_GROUP_DEFINITIONS[nutrient.primary_name]:
            children.update({child_name: _check_init_and_return(child_name)})
    # Return everything;
    return children


def _gather_all_relatives(nutrient: 'Nutrient', checked: List['Nutrient'] = None) -> Dict[str, 'Nutrient']:
    """Returns a dictionary of all relative nutrients to the named nutrient."""
    # Create a nutrient checklist to track which ones have been crawled in the tree. This prevents
    # infinite recursion;
    if checked is None:
        checked = []
    # Create list to store relatives, and temp list to append to while looping through relatives;
    relatives: Dict[str, 'Nutrient'] = {}
    to_add: Dict[str, 'Nutrient'] = {}
    # Gather the nutrients across, up and down from this nutrient;
    relatives.update(_gather_direct_siblings(nutrient))
    relatives.update(_gather_ascendants(nutrient))
    relatives.update(_gather_descendants(nutrient))
    # Add this nutrient to the checklist;
    checked.append(nutrient)
    # Now cycle through all nutrients which have not been checked yet;
    for relative in relatives.values():
        if relative not in checked:
            to_add.update(_gather_all_relatives(relative, checked))
    # Update the main list;
    relatives.update(to_add)
    # Remove myself from the list;
    relatives.pop(nutrient.primary_name, None)
    # Return everything;
    return relatives


class Nutrient:
    def __init__(self, name: str):
        self._name = main.get_nutrient_primary_name(name)

        # Add reference to myself to the list;
        main.GLOBAL_NUTRIENTS[self._name] = self

        self._direct_child_nutrients: Dict[str, 'Nutrient'] = _gather_direct_children(self)
        self._direct_parent_nutrients: Dict[str, 'Nutrient'] = _gather_direct_parents(self)
        self._all_sibling_nutrients: Dict[str, 'Nutrient'] = _gather_direct_siblings(self)
        self._all_descendant_nutrients: Dict[str, 'Nutrient'] = _gather_descendants(self)
        self._all_ascendant_nutrients: Dict[str, 'Nutrient'] = _gather_ascendants(self)
        self._all_relative_nutrients: Dict[str, 'Nutrient'] = _gather_all_relatives(self)

    @property
    def primary_name(self) -> str:
        """Returns the nutrient's primary name."""
        return self._name

    @property
    def direct_child_nutrients(self) -> Dict[str, 'Nutrient']:
        """Returns the names of the nutrient's direct children, or an empty list if there are none."""
        return self._direct_child_nutrients

    @property
    def direct_parent_nutrients(self) -> Dict[str, 'Nutrient']:
        """Returns the names of the nutrient's direct parents, or an empty list if there are none."""
        return self._direct_parent_nutrients

    @property
    def all_sibling_nutrients(self) -> Dict[str, 'Nutrient']:
        """Returns the names of the nutrient's siblings, or an empty list if there are none."""
        return self._all_sibling_nutrients

    @property
    def all_ascendant_nutrients(self) -> Dict[str, 'Nutrient']:
        """Returns the names of all ascendants to this nutrient, or an empty list if there are none."""
        return self._all_ascendant_nutrients

    @property
    def all_descendant_nutrients(self) -> Dict[str, 'Nutrient']:
        """Returns the names of all descendants of this nutrient, or an empty list if there are none."""
        return self._all_descendant_nutrients

    @property
    def all_relative_nutrients(self) -> Dict[str, 'Nutrient']:
        """Returns the names of all relatives to this nutrient, or an empty list if there are none."""
        return self._all_relative_nutrients

    @property
    def alias_names(self) -> List[str]:
        """Returns a list of aliases for the nutrient's primary name."""
        return model.nutrients.get_nutrient_alias_names(self.primary_name)

    @property
    def calories_per_g(self) -> float:
        """Returns the calories in one gram of the nutrient."""
        return model.nutrients.get_calories_per_g(self.primary_name)
