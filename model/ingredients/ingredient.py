"""Ingredient functionality module."""
import abc
from typing import Optional, List, Callable

import model
import persistence


class IngredientBase(
    model.HasMandatoryAttributes,
    model.HasReadableName,
    model.cost.HasReadableCostPerQuantity,
    model.quantity.HasReadableExtendedUnits,
    model.flags.HasReadableFlags,
    persistence.SupportsPersistence,
    abc.ABC
):
    """Abstract base class for readonly and writable ingredient classes."""

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


class ReadonlyIngredient(IngredientBase):
    """Models an ingredient with readonly attributes."""

    def __init__(self, ingredient_data_src: Callable[[], 'model.ingredients.IngredientData'], **kwargs):
        super().__init__(**kwargs)

        # Stash the callable;
        self._ingredient_data_src = ingredient_data_src

        # Populate the datafile name from the unique name;
        self._datafile_name = persistence.get_datafile_name_for_unique_value(
            cls=model.ingredients.IngredientBase,
            unique_value=self.name
        )

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
    def cost_per_qty_data(self) -> 'model.cost.CostPerQtyData':
        """Returns the cost_per_qty data for this ingredient."""
        return self._ingredient_data_src()['cost_per_qty_data']

    @property
    def flag_dofs(self) -> 'model.flags.FlagDOFData':
        """Returns the flag data for this ingredient."""
        return self._ingredient_data_src()['flag_data']

    @property
    def nutrient_ratios_data(self) -> 'model.nutrients.NutrientRatiosData':
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
    model.cost.HasSettableCostPerQuantity,
    model.quantity.HasSettableExtendedUnits,
    model.flags.HasSettableFlags,
):
    """Models an ingredient with settable attributes."""

    def __init__(self, ingredient_data: Optional['model.ingredients.IngredientData'] = None, **kwargs):
        super().__init__(**kwargs)

        if ingredient_data is not None:
            self.load_data(ingredient_data)

            # If data was passed in, then populate the datafile name;
            self._datafile_name = persistence.get_datafile_name_for_unique_value(
                cls=model.ingredients.IngredientBase,
                unique_value=self.name
            )

    @model.HasSettableName.name.setter
    def name(self, name: Optional[str]) -> None:
        """Sets name if unique to ingredient class, otherwise raises an exception."""
        # If the name is None, just set it and return;
        if name is None:
            self._name_ = name
            return

        # OK, the name isn't None, so we need to check if it is available;
        if persistence.check_unique_value_available(
            cls=self.__class__,
            proposed_value=name,
            ignore_datafile=self.datafile_name if self.datafile_name_is_defined else None
        ):
            # It is available, go ahead and set it;
            self._name_ = name
        # Otherwise, raise an exception;
        else:
            raise persistence.exceptions.UniqueValueDuplicatedError(duplicated_value=name)

    @property
    def unique_value(self) -> str:
        """Retrurns the unique value for the settable ingredient;"""
        return self._name
