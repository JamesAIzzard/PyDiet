import abc
from typing import Dict, List, Optional

import model
import persistence


class SettableIngredientQuantity(model.quantity.HasSettableQuantity, model.SupportsDefinition):
    """Models a measured quantity of an ingredient."""

    def __init__(self, ingredient: 'model.ingredients.Ingredient', **kwargs):
        super().__init__(**kwargs)

        self._ingredient: 'model.ingredients.Ingredient' = ingredient

    @property
    def ingredient(self) -> 'model.ingredients.Ingredient':
        """Returns the ingredient instance associated with the ingredient amount."""
        return self._ingredient

    def _get_quantity_in_g(self) -> Optional[float]:
        return self._quantity_in_g

    @property
    def is_defined(self) -> bool:
        return self._quantity_in_g is not None


class HasIngredientQuantities(model.quantity.HasBulk, abc.ABC):
    """Models an object which has readonly ingredient amounts."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    @abc.abstractmethod
    def ingredient_quantities(self) -> Dict[str, 'model.ingredients.IngredientQuantity']:
        """Returns a dictionary of all ingredient amounts assigned to the instance.
        The dictionary key is the ingredient amount datafile name."""
        raise NotImplementedError

    @property
    def ingredient_names(self) -> List[str]:
        """Returns a list of all the ingredients names associated with the instance."""
        return list(self.ingredient_quantities.keys())


class HasSettableIngredientQuantities(HasIngredientQuantities, persistence.HasPersistableData):
    """Models an object on which ingredient quantities can be set."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._ingredient_quantities: Dict[str, 'IngredientQuantityData']
