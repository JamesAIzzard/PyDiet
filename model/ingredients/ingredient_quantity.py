import abc
from typing import Dict, List, Optional

from model import quantity, ingredients


class IngredientQuantity(quantity.HasQuantity):
    """Models a measured quantity of an ingredient."""

    def __init__(self, ingredient: 'ingredients.Ingredient',
                 quantity_in_g: Optional[float], quantity_units: str, **kwargs):
        super().__init__(**kwargs)
        self._ingredient = ingredient

        # Store the qty data on this instance;
        self._quantity_in_g: Optional[float] = quantity_in_g
        self._quantity_pref_units: str = quantity_units

    @property
    def ingredient(self) -> 'ingredients.Ingredient':
        """Returns the ingredient instance associated with the ingredient amount."""
        return self._ingredient

    @property
    def quantity_in_g(self) -> Optional[float]:
        return self._quantity_in_g

    @property
    def quantity_pref_units(self) -> Optional[str]:
        return self._quantity_pref_units


class HasIngredientQuantities(quantity.HasBulk, abc.ABC):
    """Models an object which has readonly ingredient amounts."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    @abc.abstractmethod
    def ingredient_quantities(self) -> Dict[str, 'ingredients.IngredientQuantity']:
        """Returns a dictionary of all ingredient amounts assigned to the instance.
        The dictionary key is the ingredient amount datafile name."""
        raise NotImplementedError

    @property
    def ingredient_names(self) -> List[str]:
        """Returns a list of all the ingredients names associated with the instance."""
        return list(self.ingredient_quantities.keys())
