"""Ingredient functionality module."""
from typing import Optional, TypedDict

import model
import persistence


class IngredientData(TypedDict):
    """Ingredient data dictionary."""
    cost_per_qty_data: model.cost.CostPerQtyData
    flag_data: model.flags.FlagDOFData
    name: Optional[str]
    nutrient_ratios_data: model.nutrients.NutrientRatiosData
    extended_units_data: model.quantity.ExtendedUnitsData


class Ingredient(
    persistence.SupportsPersistence,
    model.HasName,
    model.quantity.SupportsExtendedUnits,
    model.cost.SupportsCostPerQuantity,
    model.flags.HasFlags
):
    """Readonly ingredient model."""

    def __init__(self, unique_name: Optional[str] = None, datafile_name: Optional[str] = None, **kwargs):
        # Raise an exception if no info was provided;
        if unique_name is None and datafile_name is None:
            raise ValueError("Either unique name or datafile name must be provided to init an Ingredient.")

        # OK, the unique name was provided, so use it to grab the datafile;
        elif unique_name is not None:
            super().__init__(
                name=unique_name,
                datafile_name=persistence.get_datafile_name_for_unique_value(
                    cls=model.ingredients.Ingredient,
                    unique_value=unique_name
                ),
                **kwargs
            )

        # OK, the datafile name was provided, so use it to grab the unique name;
        elif datafile_name is not None:
            super().__init__(
                name=persistence.get_unique_value_from_datafile_name(
                    cls=model.ingredients.Ingredient,
                    datafile_name=datafile_name
                ),
                datafile_name=datafile_name,
                **kwargs
            )

    @property
    def _g_per_ml(self) -> Optional[float]:
        """Returns the grams per ml for the ingredient if defined, otherwise returns None."""
        return persistence.load_datafile(
            cls=Ingredient,
            datafile_name=self.datafile_name
        )['extended_units_data']['g_per_ml']

    @property
    def _piece_mass_g(self) -> Optional[float]:
        """Returns the piece mass in grams for the ingredient, if defined, otherwise, returns None."""
        return persistence.load_datafile(
            cls=Ingredient,
            datafile_name=self.datafile_name
        )['extended_units_data']['piece_mass_g']

    @property
    def _cost_per_qty_data(self) -> 'model.cost.CostPerQtyData':
        """Returns the cost_per_qty data for this ingredient."""
        return persistence.load_datafile(
            cls=Ingredient,
            datafile_name=self.datafile_name
        )['cost_per_qty_data']

    @property
    def _flag_dofs(self) -> 'model.flags.FlagDOFData':
        """Returns the flag data for this ingredient."""
        return persistence.load_datafile(
            cls=Ingredient,
            datafile_name=self.datafile_name
        )['flag_data']

    @property
    def _nutrient_ratios_data(self) -> 'model.nutrients.NutrientRatiosData':
        """Returns the nutrient ratio data for this ingredient."""
        return persistence.load_datafile(
            cls=Ingredient,
            datafile_name=self.datafile_name
        )['nutrient_ratios_data']

    @staticmethod
    def get_path_into_db() -> str:
        """Returns the path into the ingredient database."""
        return f"{persistence.configs.path_into_db}/ingredients"

    @property
    def unique_value(self) -> str:
        """Returns the ingredient's unique name."""
        return self.name

    @property
    def persistable_data(self) -> 'model.ingredients.IngredientData':
        """Returns the persistable data for the ingredient instance."""
        return super().persistable_data
