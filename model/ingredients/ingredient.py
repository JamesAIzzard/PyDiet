"""Ingredient functionality module."""
import abc
from typing import Optional, TypedDict, List, Callable

import model
import persistence


class IngredientData(TypedDict):
    """Ingredient data dictionary."""
    cost_per_qty_data: model.cost.CostPerQtyData
    flag_data: model.flags.FlagDOFData
    name: Optional[str]
    nutrient_ratios_data: model.nutrients.NutrientRatiosData
    extended_units_data: model.quantity.ExtendedUnitsData


class IngredientBase(
    model.HasMandatoryAttributes,
    model.HasName,
    model.cost.SupportsCostPerQuantity,
    model.quantity.SupportsExtendedUnits,
    model.flags.HasFlags,
    persistence.SupportsPersistence,
    abc.ABC
):
    """Base class to host common functionality shared between Ingredient and Settable Ingredient."""

    @property
    def missing_mandatory_attrs(self) -> List[str]:
        """Returns a list of undefined mandatory properties on the ingredient."""
        # Create a list to store the results;
        missing_attrs: List[str] = []

        # Check the name;
        if not self.name_is_defined:
            missing_attrs.append("name")

        # Check the cost;
        if not self.cost_is_defined:
            missing_attrs.append("cost")

        # Check for any missing mandatory nutrients;
        missing_nrs = self.undefined_mandatory_nutrient_ratio_names
        if len(missing_nrs) > 0:
            missing_attrs += missing_nrs

        # Return the list of missing attributes;
        return missing_attrs

    @staticmethod
    def get_path_into_db() -> str:
        """Returns the path into the ingredient database."""
        return f"{persistence.configs.path_into_db}/ingredients"


class Ingredient(
    IngredientBase,
):
    """Models an ingredient with readonly attributes."""

    def __init__(self, ingredient_data_src: Callable[[], 'IngredientData'], **kwargs):
        super().__init__(**kwargs)

        # Stash the callable;
        self._ingredient_data_src = ingredient_data_src

    @property
    def _name(self) -> Optional[str]:
        """Returns the ingredient's name if defined, otherwise returns None."""
        return self._ingredient_data_src()['name']

    @property
    def _g_per_ml(self) -> Optional[float]:
        """Returns the grams per ml for the ingredient if defined, otherwise returns None."""
        return self._ingredient_data_src()['extended_units_data']['g_per_ml']

    @property
    def _piece_mass_g(self) -> Optional[float]:
        """Returns the piece mass in grams for the ingredient, if defined, otherwise, returns None."""
        return self._ingredient_data_src()['extended_units_data']['piece_mass_g']

    @property
    def _cost_per_qty_data(self) -> 'model.cost.CostPerQtyData':
        """Returns the cost_per_qty data for this ingredient."""
        return self._ingredient_data_src()['cost_per_qty_data']

    @property
    def _flag_dofs(self) -> 'model.flags.FlagDOFData':
        """Returns the flag data for this ingredient."""
        return self._ingredient_data_src()['flag_data']

    @property
    def _nutrient_ratios_data(self) -> 'model.nutrients.NutrientRatiosData':
        """Returns the nutrient ratio data for this ingredient."""
        return self._ingredient_data_src()['nutrient_ratios_data']

    @property
    def persistable_data(self) -> 'model.ingredients.IngredientData':
        """Returns the persistable data for the ingredient instance."""
        return super().persistable_data

    @property
    def unique_value(self) -> str:
        """Returns the ingredient's unique name."""
        return self._ingredient_data_src()['name']


class SettableIngredient(
    IngredientBase,
    model.HasSettableName,
    model.cost.SupportsSettableCostPerQuantity,
    model.quantity.SupportsExtendedUnitSetting,
    model.flags.HasSettableFlags,
):
    """Models an ingredient with settable attributes."""

    def __init__(self, ingredient_data: Optional['IngredientData'] = None, **kwargs):
        super().__init__(**kwargs)

        if ingredient_data is not None:
            self.load_data(ingredient_data)

    @property
    def unique_value(self) -> str:
        """Retrurns the unique value for the settable ingredient;"""
        return self._name
