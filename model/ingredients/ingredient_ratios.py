"""Implements the functionality associated with ingredient ratios."""
import abc
from typing import List, Dict, Callable, Optional

import model
import persistence


class IngredientRatioBase(
    model.quantity.IsQuantityRatioBase,
    persistence.YieldsPersistableData,
    abc.ABC
):
    """Abstract base class for readonly and writeable nutrient ratios."""

    def __init__(self, ingredient: 'model.ingredients.IngredientBase', **kwargs):
        if not isinstance(ingredient, model.ingredients.IngredientBase):
            raise TypeError("Ingredient must be an subclass of IngredientBase.")

        super().__init__(ratio_subject=ingredient, **kwargs)


class ReadonlyIngredientRatio(IngredientRatioBase, model.quantity.IsReadonlyQuantityRatio):
    """Models a readonly ingredient ratio."""


class HasReadableIngredientRatios(abc.ABC):
    """Mixin to implement functionality associated with having readable ingredient ratios."""

    @property
    @abc.abstractmethod
    def ingredient_ratios_data(self) -> 'model.ingredients.IngredientRatiosData':
        """Returns the ingredient ratios data associated with this instance."""
        raise NotImplementedError

    @property
    def ingredient_ratios(self) -> Dict[str, 'ReadonlyIngredientRatio']:
        """Returns the ingredient ratio instances associated with this instance."""
        # Create a dict to compile the ratios;
        irs: Dict[str, 'ReadonlyIngredientRatio'] = {}

        # Create an factory function to make accessors for the qty data;
        def get_qty_ratio_data_src(ingredient_datafile_name: str) -> Callable[[], 'model.quantity.QuantityRatioData']:
            """Returns a src function for the named ingredient qty ratio data."""
            return lambda: self.ingredient_ratios_data[ingredient_datafile_name]

        # Compile the ratios;
        for idf_name, ratio_data in self.ingredient_ratios_data.items():
            irs[idf_name] = self.get_ingredient_ratio(
                ingredient_df_name=idf_name
            )

        # Return
        return irs

    def get_ingredient_ratio(
            self,
            ingredient_unique_name: Optional[str] = None,
            ingredient_df_name: Optional[str] = None
    ) -> 'ReadonlyIngredientRatio':
        """Returns an ingredient ratio by name."""
        # Handle the arguments;
        if ingredient_df_name is None and ingredient_unique_name is None:
            raise ValueError("Either ingredient unique name or df name must be provided.")
        elif ingredient_df_name is None:
            ingredient_df_name = model.ingredients.get_df_name_from_ingredient_name(ingredient_unique_name)

        # Create and return the instance;
        return ReadonlyIngredientRatio(
            ingredient=model.ingredients.ReadonlyIngredient(
                ingredient_data_src=model.ingredients.get_ingredient_data_src(
                    for_df_name=ingredient_df_name
                )
            ),
            ratio_host=self,
            qty_ratio_data_src=lambda: self.ingredient_ratios_data[ingredient_df_name]
        )

    @property
    def ingredient_unique_names(self) -> List[str]:
        """Returns a list of the ingredient names associated with the instance."""
        names: List[str] = []

        for ingredient_df_name in self.ingredient_ratios_data.keys():
            names.append(model.ingredients.get_ingredient_name_from_df_name(ingredient_df_name))

        return names
