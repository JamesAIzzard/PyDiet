"""Defines functionality related to ingredient quantities."""
import abc
from typing import Dict, List, Optional, Any

import model
import persistence

IngredientQuantitiesData = Dict[str, model.quantity.QuantityData]


class IngredientQuantity(model.quantity.QuantityOf):
    """Models a readonly quantity of an ingredient."""

    def __init__(self, ingredient: 'model.ingredients.Ingredient', **kwargs):
        super().__init__(subject=ingredient, **kwargs)

    @property
    def ingredient(self) -> 'model.ingredients.Ingredient':
        """Returns the ingredient instance associated with the ingredient amount."""
        return self._subject


class SettableIngredientQuantity(IngredientQuantity, model.quantity.SettableQuantityOf):
    """Models a settable quantity of an ingredient."""


class HasIngredientQuantities(persistence.YieldsPersistableData, abc.ABC):
    """Models an object which has readonly quantities of ingredients."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def ingredient_quantities(self) -> Dict[str, 'model.ingredients.IngredientQuantity']:
        """Returns a dictionary of all ingredient amounts assigned to the instance.
        The dictionary key is the ingredient amount datafile name."""
        raise NotImplementedError

    @property
    def ingredient_names(self) -> List[str]:
        """Returns a list of all the ingredients names associated with the instance."""
        return list(self.ingredient_quantities.keys())

    @property
    def persistable_data(self) -> Dict[str, Any]:
        data = super().persistable_data
        for ingredient_df_name, ingredient_quantity in self.ingredient_quantities.items():
            data['ingredient_quantities_data'][ingredient_df_name] = ingredient_quantity.persistable_data
        return data


class HasSettableIngredientQuantities(HasIngredientQuantities):
    """Models an object on which ingredient quantities can be set."""

    def __init__(self, ingredient_quantities_data: Optional[Dict[str, 'model.quantity.QuantityData']] = None, **kwargs):
        super().__init__(**kwargs)

        self._ingredient_quantities: Dict[str, 'IngredientQuantity']

