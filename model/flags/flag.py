import enum, abc
from typing import Dict, Optional

from model import nutrients


class FlagImpliesNutrient(enum.Enum):
    NON_ZERO = 1
    ZERO = 0


class AbstractFlag(abc.ABC):
    """Class to define the interface of flag objects.
    This perhaps seems like an unescessary overcomplication, but by defining an interface here, we
    open the possibility of having custom implementations of highly specialised flags, with their
    own logic.
    To create a custom implementation, inherit from this class, and overwrite the __bool__ method
    and set method with the custom logic.
    """

    @abc.abstractmethod
    def name(self) -> str:
        """Returns the flag name."""

    @property
    @abc.abstractmethod
    def value(self) -> Optional[bool]:
        """Calculates/returns the flags current value, based on nutrient states and own DOF."""

    @abc.abstractmethod
    def set_value(self, value: Optional[bool]) -> None:
        """Sets the flag value."""


class Flag(AbstractFlag):
    """Models a food flag."""

    def __init__(self, name: str,
                 nutrient_relations: Optional[Dict[str, 'FlagImpliesNutrient']] = None,
                 direct_alias: bool = False):
        """
        Args:
            name: The flag name.
            nutrient_relations (Dict[str, 'FlagImpliesNutrient']): Dictionary of related nutrient names,
                and what the True flag would imply about the mass of the named nutrient in the subject.
            direct_alias (bool): Indicates if the flag is completely defined by its nutrient relations.
        """
        # Check the object has nutrient ratios too;
        if not isinstance(self, nutrients.HasNutrientRatios):
            raise AttributeError("Flags cannot be used without nutrient ratios.")

        # Dissallow direct alias if there are no nutrient relations;
        if direct_alias and len(nutrient_relations) == 0:
            raise ValueError("A flag cannot be a direct alias without nutrient relations.")

        self._name = name
        self._nutrient_relations = {}
        self._direct_alias = direct_alias
        self._dof: Optional[bool] = None
        for nutrient_name, implication in nutrient_relations.items():
            nutrient_name = nutrients.get_nutrient_primary_name(nutrient_name)
            self._nutrient_relations[nutrient_name] = implication

    @property
    def name(self) -> str:
        return self._name

    def set_value(self, value: Optional[bool]) -> None:
        """Sets the flag's value."""
        if isinstance(self, nutrients.HasSettableNutrientRatios):
            for nutrient_name, implication in self._nutrient_relations.items():
                if implication == FlagImpliesNutrient.ZERO:
                    self.set_nutrient_ratio(nutrient_name, 0, 'g', 100, 'g')
                elif implication == FlagImpliesNutrient.NON_ZERO:
                    if self.get_nutrient_ratio(nutrient_name):
                        ...

    @property
    def value(self) -> Optional[bool]:
        """Returns True/False to indicate if the flag is True/False for the given object."""
        nut_match = self.nutrients_match_implied_states  # Cache this value.
        # Regardless of direct_alias, if a single nutrient disagrees with flag, return False:
        if nut_match is False:
            return False
        if self._direct_alias:
            if nut_match is True:  # All nutrients match positively.
                return True
            elif nut_match is None:  # At least one nutrient is undefined.
                return None
        elif not self._direct_alias:  # No nutrients disagree, so defer to dof.
            return self._dof

    @property
    def nutrients_match_implied_states(self) -> Optional[bool]:
        """Returns True if all nutrients match implied states. Returns False is any nutrient
        conflicts with implied state. Returns None if a related nutrient is undefined.
        """
        # Check we have readable nutrients;
        if not isinstance(self, nutrients.HasNutrientRatios):
            raise AttributeError("Flags cannot be used without nutrient ratios.")

        undefined_found = False

        for nut_name, implication in self._nutrient_relations.items():
            nutrient_ratio = self.get_nutrient_ratio(nutrient_name=nut_name)

            # If a nutrient is undefined, log it.
            # We don't return undefined immediatley, because we still want to check for hard conflicts.
            if nutrient_ratio.undefined:
                undefined_found = True
                continue
            # Now we know the nutrient is defined, check if nutrient matches implication;
            if implication is FlagImpliesNutrient.ZERO and nutrient_ratio.is_non_zero:
                return False
            elif implication is FlagImpliesNutrient.NON_ZERO and nutrient_ratio.is_zero:
                return False

            # Check next.

        # No disagreements found;
        if undefined_found:
            return None
        else:
            return True
