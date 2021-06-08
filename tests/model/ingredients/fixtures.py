"""Fixtures for ingredient module testing."""
from typing import Dict, Optional, Any

import model
import persistence
from tests.model.cost import fixtures as cfx
from tests.model.quantity import fixtures as qfx

INGREDIENT_NAME_WITH = {
    "name_raspberry": "Raspberry",
    "typical_fully_defined_data": "Raspberry",
    "density_defined": "Lemon Juice",
    "density_undefined": "Aubergine",
    "piece_mass_defined": "Aubergine",
    "piece_mass_undefined": "Lemon Juice",
    "cost_per_g_defined": "Aubergine",
    "cost_per_g_undefined": "Courgette",
    "flag_dofs_all_defined": "Spinach",
    "flag_dofs_two_undefined": "Lemon",
    "nutrient_ratios_protein_defined": "Smoked Salmon",
    "nutrient_ratios_iron_undefined": "Smoked Salmon",
    "nutrient_ratios_8_ratios_defined": "Red Pepper",
    "nutrient_ratios_protein_carbs_undefined": "Bacon",
    "7.2_calories_per_g": "Pine Nuts",
    "14_grams_of_protein_per_100_g": "Pine Nuts"
}


class IngredientBaseTestable(model.ingredients.IngredientBase):
    """Minimal implementation to allow BaseIngredient testing."""

    def __init__(self, ingredient_data: 'model.ingredients.IngredientData', **kwargs):
        super().__init__(**kwargs)

        # Init the data locally to return during tests;
        self._ingredient_data = ingredient_data

    @property
    def _name(self) -> Optional[str]:
        """Returns instance name."""
        return self._ingredient_data['name']

    @property
    def cost_per_qty_data(self) -> 'model.cost.CostPerQtyData':
        """Returns instance cost data."""
        return self._ingredient_data['cost_per_qty_data']

    @property
    def _g_per_ml(self) -> Optional[float]:
        """Returns instance g_per_ml."""
        return self._ingredient_data['extended_units_data']['g_per_ml']

    @property
    def _piece_mass_g(self) -> Optional[float]:
        """Returns instance pc mass."""
        return self._ingredient_data['extended_units_data']['piece_mass_g']

    @property
    def flag_dofs(self) -> 'model.flags.FlagDOFData':
        """Returns instance flag data."""
        return self._ingredient_data['flag_data']

    @property
    def nutrient_ratios_data(self) -> 'model.nutrients.NutrientRatiosData':
        """Returns instance's nutrient ratios data."""
        return self._ingredient_data['nutrient_ratios_data']

    @property
    def unique_value(self) -> str:
        """Returns instance's unique value, in this case name."""
        return self._ingredient_data['name']


class IngredientRatioBaseTestable(model.ingredients.IngredientRatioBase):
    """Minimal implementation to allow testing of the IngredientRatioBase class."""

    def __init__(
            self,
            ingredient: 'model.ingredients.ReadonlyIngredient',
            host: Any,
            qty_ratio_data: 'model.quantity.QuantityRatioData'
    ):
        super().__init__(ratio_subject=ingredient, ratio_host=host)
        self._quantity_ratio_data = qty_ratio_data

    @property
    def quantity_ratio_data(self) -> 'model.quantity.QuantityRatioData':
        """Return the qty ratio data."""
        return self._quantity_ratio_data


class HasReadableIngredientQuantitiesTestable(model.ingredients.HasReadableIngredientQuantities):
    """Minimal implementation to test the HasIngredientQuantities class."""

    def __init__(self, ingredient_quantities_data: 'model.ingredients.IngredientQuantitiesData', **kwargs):
        super().__init__(**kwargs)

        # Stash the ingredient quantities data;
        self._ingredient_quantities_data = ingredient_quantities_data

    @property
    def ingredient_quantities(self) -> Dict[str, 'model.ingredients.ReadonlyIngredientQuantity']:
        """Returns the ingredient quantities data."""
        # Somewhere to compile the riq instances;
        iqs = {}

        # Create func to access data from iq line;
        def get_qty_data_src(idf_name):
            """Accessor for quantity data from dict."""
            return lambda: self._ingredient_quantities_data[idf_name]

        # Cycle through the data, and compile;
        for df_name, q_data in self._ingredient_quantities_data.items():
            iqs[df_name] = model.ingredients.ReadonlyIngredientQuantity(
                ingredient=model.ingredients.ReadonlyIngredient(
                    ingredient_data_src=get_ingredient_data_src(for_ingredient_df_name=df_name),
                ),
                quantity_data_src=get_qty_data_src(df_name)
            )

        # Return the compiled list;
        return iqs


def get_ingredient_name_with(characteristic: str) -> str:
    """Returns an ingredient name matching the specified characteristic.
    Performs a lookup on the table above.
    """
    return INGREDIENT_NAME_WITH[characteristic]


def get_ingredient_df_name(unique_name: str) -> str:
    """Returns the ingredient datafile name corresponding the the unique name provided."""
    return persistence.get_datafile_name_for_unique_value(
        cls=model.ingredients.IngredientBase,
        unique_value=unique_name
    )


def get_ingredient_data_src(
        for_ingredient_unique_name: Optional[str] = None,
        for_ingredient_df_name: Optional[str] = None
):
    """Returns a callable that returns ingredient data.
    Args:
        for_ingredient_df_name: When specified, returns callable data src for ingredient specified by
            this datafile name.
        for_ingredient_unique_name (Optional[str]): When specified, returns callable for data corresponding
            this particular name.
    """
    if for_ingredient_unique_name is not None:
        return lambda: get_ingredient_data(for_unique_name=for_ingredient_unique_name)
    elif for_ingredient_df_name is not None:
        return lambda: get_ingredient_data(for_df_name=for_ingredient_df_name)


def get_ingredient_data(
        for_unique_name: Optional[str] = None,
        for_df_name: Optional[str] = None,
):
    """Returns ingredient data.
    Args:
        for_df_name (Optional[str]): When specified, loads and returns data corresponding to this datafile name.
        for_unique_name (Optional[str]): When specified, loads and returns data corresponding to this particular name.
    """
    # If a unique name was specified;
    if for_unique_name is not None:
        # Fetch the data corresponding to that name;
        return persistence.load_datafile(cls=model.ingredients.ReadonlyIngredient, unique_value=for_unique_name)

    # If a df name was specified;
    if for_df_name is not None:
        # Fetch the data corresponding to that name;
        return persistence.load_datafile(cls=model.ingredients.IngredientBase, datafile_name=for_df_name)

    # If nothing was specifed;
    return model.ingredients.IngredientData(
        cost_per_qty_data=cfx.get_cost_per_qty_data(),
        flag_data={},
        name=None,
        nutrient_ratios_data={},
        extended_units_data=qfx.get_extended_units_data()
    )


def get_ingredient_ratio_data(
        ingredient_qty_g: Optional[float] = None,
        ingredient_qty_unit: str = 'g',
        host_qty_g: Optional[float] = None,
        host_qty_unit: str = 'g'
) -> 'model.ingredients.IngredientRatioData':
    """Creates an ingredient qty data instance, applying defaults if values not specified."""
    return model.ingredients.IngredientRatioData(
        subject_qty_data=model.quantity.QuantityData(
            quantity_in_g=ingredient_qty_g,
            pref_unit=ingredient_qty_unit
        ),
        host_qty_data=model.quantity.QuantityData(
            quantity_in_g=host_qty_g,
            pref_unit=host_qty_unit
        )
    )
