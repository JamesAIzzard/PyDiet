from typing import Dict, List, Callable, Optional, Any

import model
import persistence


class IngredientQuantityOf(model.quantity.HasQuantityOf, model.SupportsDefinition):
    """Models a readonly quantity of an ingredient."""

    def __init__(self, ingredient: 'model.ingredients.Ingredient', **kwargs):
        super().__init__(subject=ingredient, **kwargs)

    @property
    def ingredient(self) -> 'model.ingredients.Ingredient':
        """Returns the ingredient instance associated with the ingredient amount."""
        assert (isinstance(self._subject, model.ingredients.Ingredient))
        return self._subject

    @property
    def is_defined(self) -> bool:
        return self._get_quantity_in_g() is not None


class SettableIngredientQuantity(IngredientQuantityOf, model.quantity.HasSettableQuantityOf):
    """Models a settable quantity of an ingredient."""


class HasIngredientQuantities:
    """Models an object which has readonly quantities of ingredients."""

    def __init__(self, get_ingredient_quantities: Callable[[], Dict[str, 'IngredientQuantityOf']], **kwargs):
        super().__init__(**kwargs)

        self._get_ingredient_quantities = get_ingredient_quantities

    @property
    def ingredient_quantities(self) -> Dict[str, 'model.ingredients.IngredientQuantityOf']:
        """Returns a dictionary of all ingredient amounts assigned to the instance.
        The dictionary key is the ingredient amount datafile name."""
        return self._get_ingredient_quantities()

    @property
    def ingredient_names(self) -> List[str]:
        """Returns a list of all the ingredients names associated with the instance."""
        return list(self.ingredient_quantities.keys())

    @property
    def persistable_data(self) -> Dict[str, Any]:
        data = {}
        for ingredient_df_name, ingredient_quantity in self.ingredient_quantities.items():
            data[ingredient_df_name] = ingredient_quantity.persistable_data
        return data


class HasSettableIngredientQuantities(HasIngredientQuantities):
    """Models an object on which ingredient quantities can be set."""

    def __init__(self, ingredient_quantities_data: Optional[Dict[str, 'model.quantity.QuantityData']] = None, **kwargs):
        super().__init__(**kwargs)

        self._ingredient_quantities: Dict[str, 'model.quantity.QuantityData']

