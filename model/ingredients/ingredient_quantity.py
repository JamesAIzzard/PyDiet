"""Defines functionality related to ingredient quantities."""
import abc
from typing import Dict, Optional, Any

import model
import persistence
from .ingredient_ratios import HasReadableIngredientRatios


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


class HasReadableIngredientQuantities(
    HasReadableIngredientRatios,
    persistence.YieldsPersistableData,
    abc.ABC
):
    """Models an object which has readable ingredient quantities."""

    @property
    @abc.abstractmethod
    def ingredient_quantities_data(self) -> 'model.ingredients.IngredientQuantitiesData':
        """Returns the ingredient quantities data for the instance."""
        raise NotImplementedError

    @property
    def ingredient_ratios_data(self) -> 'model.ingredients.IngredientRatiosData':
        """Returns the ingredient ratios data associated with this instance."""
        ird: 'model.ingredients.IngredientRatiosData' = {}
        total_ingredient_quantity = self.total_ingredients_mass_g
        for df_name, iq in self.ingredient_quantities.items():
            ird[df_name] = model.quantity.QuantityRatioData(
                subject_qty_data=model.quantity.QuantityData(
                    quantity_in_g=iq.quantity_in_g,
                    pref_unit='g'
                ),
                host_qty_data=model.quantity.QuantityData(
                    quantity_in_g=total_ingredient_quantity,
                    pref_unit='g'
                )
            )

        return ird

    @property
    def ingredient_quantities(self) -> Dict[str, 'model.ingredients.ReadonlyIngredientQuantity']:
        """Returns the readonly ingredient quantities on the instance."""
        # Cache the ingredient quantities data;
        iq_data = self.ingredient_quantities_data

        # Create dict to compile the ingredient quantites;
        iq = {}

        # Define an accessor func for the qty data src;
        def get_qty_data_src(df_name):
            """Accessor function for ingredient data src."""
            return lambda: iq_data[df_name]

        # Cycle through the data and init the ingredient quantities;
        for i_df_name, iqo_data in iq_data.items():
            # noinspection PyTypeChecker
            iq[i_df_name] = model.ingredients.ReadonlyIngredientQuantity(
                ingredient=model.ingredients.ReadonlyIngredient(
                    ingredient_data_src=model.ingredients.get_ingredient_data_src(
                        for_df_name=i_df_name
                    ),
                ),
                quantity_data_src=get_qty_data_src(i_df_name)
            )

        # Return the dict;
        return iq

    @property
    def total_ingredients_mass_g(self) -> float:
        """Returns the total mass (in g) of the ingredients associated with this instnace."""
        tot = 0
        for iq in self.ingredient_quantities.values():
            tot += iq.quantity_in_g
        return tot

    def get_nutrient_mass(self, nutrient_name:str) -> 'model.nutrients.NutrientMassData':
        """Returns the nutrient mass for single nutrient."""
        nutrient_name = model.nutrients.validation.validate_nutrient_name(nutrient_name)
        return model.quantity.QuantityData(
            quantity_in_g=self.get_nutrient_ratio(
                nutrient_name).subject_g_per_host_g * self.total_ingredients_mass_g,
            pref_unit='g'
        )

    @property
    def nutrient_masses(self) -> Dict[str, 'model.nutrients.NutrientMassData']:
        """Returns nutrient masses for all defined nutrients."""
        nms = {nut_name: model.quantity.QuantityData(quantity_in_g=0, pref_unit='g') for nut_name in
               self.defined_nutrient_ratio_names}
        for nutr_name in nms.keys():
            nms[nutr_name]['quantity_in_g'] = self.get_nutrient_ratio(
                nutr_name).subject_g_per_host_g * self.total_ingredients_mass_g
        return nms

    @property
    def num_calories(self) -> float:
        """Returns the number of calories associated with this instance."""
        return self.calories_per_g * self.total_ingredients_mass_g

    @property
    def persistable_data(self) -> Dict[str, Any]:
        """Returns the instance's persistable data."""
        # Collect the persistable data from the superclass.
        data = super().persistable_data

        # Now add an ingredient_quantities data field;
        data['ingredient_quantities_data'] = self.ingredient_quantities_data

        # Return the updated data dict;
        return data


class HasSettableIngredientQuantities(HasReadableIngredientQuantities, persistence.CanLoadData):
    """Models an object on which ingredient quantities can be set."""

    def __init__(self, ingredient_quantities_data: Optional[Dict[str, 'model.quantity.QuantityData']] = None, **kwargs):
        super().__init__(**kwargs)

        # Init local storage for ingredient quantities;
        self._ingredient_quantities_data: Dict[str, 'model.quantity.QuantityData'] = {}

        # If data was provided, load it;
        if ingredient_quantities_data is not None:
            self.load_data({'ingredient_quantities_data': ingredient_quantities_data})

    @property
    def ingredient_quantities_data(self) -> Dict[str, 'model.quantity.QuantityData']:
        """Returns the ingredient quantities associated with the instance."""
        return self._ingredient_quantities_data

    @property
    def ingredient_quantities(self) -> Dict[str, 'model.ingredients.SettableIngredientQuantity']:
        """Returns the readonly ingredient quantities on the instance."""

        # Create dict to compile the ingredient quantites;
        iq = {}

        # Cycle through the data and init the ingredient quantities;
        for i_df_name, iqo_data in self._ingredient_quantities_data.items():
            # noinspection PyTypeChecker
            iq[i_df_name] = model.ingredients.SettableIngredientQuantity(
                ingredient=model.ingredients.ReadonlyIngredient(
                    ingredient_data_src=model.ingredients.get_ingredient_data_src(
                        for_df_name=i_df_name
                    )),
                quantity_data=iqo_data
            )

        # Return the dict;
        return iq

    def add_ingredient_quantity(self, ingredient_unique_name, qty_value, qty_unit) -> None:
        """Adds an ingredient quantity to the instance.
        Notes:
           We actually create the instance here, to ensure there are no validation issues.
        """

        # Fetch the ingredient instance;
        i = model.ingredients.ReadonlyIngredient(
            ingredient_data_src=lambda: persistence.load_datafile(
                cls=model.ingredients.IngredientBase,
                unique_value=ingredient_unique_name
            )
        )

        # Create the ingredient quantity instance;
        iq = SettableIngredientQuantity(ingredient=i)
        iq.set_quantity(quantity_value=qty_value, quantity_unit=qty_unit)

        # Add the ingredient to the dict;
        self._ingredient_quantities_data[i.datafile_name] = iq.persistable_data

    def load_data(self, data: Dict[str, Any]) -> None:
        """Loads data into the instance."""
        # Load data on the superclass;
        super().load_data(data)

        # If there is an ingredient quantities heading in the data;
        if 'ingredient_quantities_data' in data.keys():
            # Go ahead and stash it locally;
            self._ingredient_quantities_data = data['ingredient_quantities_data']
