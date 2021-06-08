"""Defines functionality related to ingredient quantities."""
import abc
from typing import Dict, List, Callable, Optional, Any

import model
import persistence


class IngredientQuantityBase(
    model.nutrients.HasReadableNutrientMasses,
    model.quantity.IsQuantityOfBase,
    abc.ABC
):
    """Abstract base class for readonly and writable ingredient quantity classes."""

    def __init__(self, ingredient: 'model.ingredients.ReadonlyIngredient', **kwargs):

        if not isinstance(ingredient, model.ingredients.ReadonlyIngredient):
            raise TypeError("Ingredient arg must be a ReadonlyIngredient instance.")

        super().__init__(qty_subject=ingredient, **kwargs)

    @property
    def ingredient(self) -> 'model.ingredients.ReadonlyIngredient':
        """Returns the ingredient instance associated with the ingredient amount."""
        return self._qty_subject


class ReadonlyIngredientQuantity(IngredientQuantityBase, model.quantity.IsReadonlyQuantityOf):
    """Models a readonly quantity of an ingredient."""


class SettableIngredientQuantity(IngredientQuantityBase, model.quantity.IsSettableQuantityOf):
    """Models a settable quantity of an ingredient."""


class HasReadableIngredientQuantities(persistence.YieldsPersistableData, abc.ABC):
    """Models an object which has readable ingredient quantities."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    @abc.abstractmethod
    def ingredient_quantities(self) -> Dict[str, 'model.ingredients.ReadonlyIngredientQuantity']:
        """Returns a dictionary of all ingredient amounts assigned to the instance.
        The dictionary key is the ingredient amount datafile name."""
        raise NotImplementedError

    @property
    def ingredient_unique_names(self) -> List[str]:
        """Returns a list of all the ingredients names associated with the instance."""
        # Create a list to compile the unique names;
        unique_names = []

        # Work through the quantities list, and populate the unique names using the df names;
        for df_name in self.ingredient_quantities.keys():
            unique_names.append(persistence.get_unique_value_from_datafile_name(
                cls=model.ingredients.IngredientBase,
                datafile_name=df_name
            ))

        # Convert list-set to eliminate dupiclates, and return;
        return list(set(unique_names))

    @property
    def persistable_data(self) -> Dict[str, Any]:
        """Returns the instance's persistable data."""
        # Collect the persistable data from the superclass.
        data = super().persistable_data

        # Now add an ingredient_quantities data field;
        data['ingredient_quantities_data'] = {}
        # Now populate the field;
        for ingredient_df_name, ingredient_quantity in self.ingredient_quantities.items():
            data['ingredient_quantities_data'][ingredient_df_name] = ingredient_quantity.persistable_data

        # Return the updated data dict;
        return data


class HasSettableIngredientQuantities(HasReadableIngredientQuantities, persistence.CanLoadData):
    """Models an object on which ingredient quantities can be set."""

    def __init__(self, ingredient_quantities_data: Optional[Dict[str, 'model.quantity.QuantityData']] = None, **kwargs):
        super().__init__(**kwargs)

        # Init local storage for ingredient quantities;
        self._ingredient_quantities: Dict[str, 'SettableIngredientQuantity'] = {}

        # If data was provided, load it;
        if ingredient_quantities_data is not None:
            self.load_data({'ingredient_quantities_data': ingredient_quantities_data})

    @property
    def ingredient_quantities(self) -> Dict[str, 'model.ingredients.SettableIngredientQuantity']:
        """Returns the ingredient quantities associated with the instance."""
        return self._ingredient_quantities

    def load_data(self, data: Dict[str, Any]) -> None:
        """Loads data into the instance."""
        # Load data on the superclass;
        super().load_data(data)

        # Create a factory funtion to return access functions for the ingredient data;
        def get_ingredient_data_src(df_name: str) -> Callable[[], 'model.ingredients.IngredientData']:
            """Factory function to return data access callable."""
            return lambda: persistence.load_datafile(
                cls=model.ingredients.IngredientData,
                datafile_name=df_name
            )

        # If there is an ingredient quantities heading in the data;
        if 'ingredient_quantities_data' in data.keys():
            # Go ahead and populate the local dictionary;
            for ingredient_df_name, ingredient_quantity_data in data['ingredient_quantities_data'].items():
                self._ingredient_quantities[ingredient_df_name] = SettableIngredientQuantity(
                    ingredient=model.ingredients.ReadonlyIngredient(
                        ingredient_data_src=get_ingredient_data_src(df_name=ingredient_df_name)
                    ),
                    quantity_data=model.quantity.QuantityData(
                        quantity_in_g=ingredient_quantity_data['quantity_in_g'],
                        pref_unit=ingredient_quantity_data['pref_unit']
                    )
                )
