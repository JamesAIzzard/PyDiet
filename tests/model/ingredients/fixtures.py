"""Fixtures for ingredient module testing."""
from typing import Optional, Any, Dict

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


class IngredientTestable(model.ingredients.ReadableIngredient):
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
            host: Any,
            subject: Any,
            ratio_data: 'model.quantity.QuantityRatioData'
    ):
        self._host = host
        self._subject = subject
        self._ratio_data = ratio_data

    @property
    def ingredient_qty(self) -> 'model.ingredients.ReadonlyIngredientQuantity':
        """Returns the ingredient quantity instance."""
        return model.ingredients.ReadonlyIngredientQuantity(
            ingredient=self._subject,
            quantity_data_src=qfx.get_qty_data_src(quantity_data=qfx.get_qty_data(
                qty_in_g=self._ratio_data['subject_qty_data']['quantity_in_g'],
                pref_unit=self._ratio_data['subject_qty_data']['pref_unit']
            ))
        )

    @property
    def subject_ref_qty(self) -> 'model.quantity.HasReadableQuantityOf':
        """Returns the subject ref qty instance."""
        return model.quantity.HasReadonlyQuantityOf(
            qty_subject=self._host,
            quantity_data_src=qfx.get_qty_data_src(quantity_data=qfx.get_qty_data(
                qty_in_g=self._ratio_data['host_qty_data']['quantity_in_g'],
                pref_unit=self._ratio_data['host_qty_data']['pref_unit']
            ))
        )

    @property
    def persistable_data(self) -> Dict[str, Any]:
        pass



def get_ingredient_name_with(characteristic: str) -> str:
    """Returns an ingredient name matching the specified characteristic.
    Performs a lookup on the table above.
    """
    return INGREDIENT_NAME_WITH[characteristic]


def get_ingredient_data_src(
        for_ingredient_name: Optional[str] = None
):
    """Returns a callable that returns ingredient data.
    Args:
        for_ingredient_name (Optional[str]): When specified, returns callable for data corresponding
            this particular name.
    """
    return lambda: get_ingredient_data(for_unique_name=for_ingredient_name)


def get_ingredient_data(
        for_unique_name: Optional[str] = None
):
    """Returns ingredient data.
    Args:
        for_unique_name (Optional[str]): When specified, loads and returns data corresponding to this particular name.
    """
    # If a unique name was specified;
    if for_unique_name is not None:
        # Fetch the data corresponding to that name;
        return persistence.load_datafile(cls=model.ingredients.ReadonlyIngredient, unique_value=for_unique_name)

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
