"""Defines recipe classes."""
import abc
from typing import Callable, Optional, Dict, List, Any

import model
import persistence


class RecipeBase(
    model.HasReadableName,
    model.ingredients.HasReadableIngredientQuantities,
    model.time.HasReadableServeIntervals,
    model.instructions.HasReadableInstructionSrc,
    model.tags.HasReadableTags,
    persistence.SupportsPersistence,
    abc.ABC
):
    """Abstract base class for readable and writbale recipe classes."""

    @property
    def unique_value(self) -> str:
        """Returns the unique name of the recipe."""
        return self._name

    @property
    def defined_nutrient_ratio_names(self) -> List[str]:
        """Returns a list of all of the nutrient names corresponding to nutrient ratios defined
        on the instance."""
        return list(self.nutrient_ratios_data.keys())

    def get_nutrient_ratio(self, nutrient_name: str) -> 'model.nutrients.ReadonlyNutrientRatio':
        """Returns a ReadableNutrientRatio by name."""
        # Convert to the primary name, in case we were given an alias;
        nutrient_name = model.nutrients.get_nutrient_primary_name(nutrient_name)

        # If the nutrient is defined (i.e if it is in the dictionary);
        if nutrient_name in self.nutrient_ratios_data.keys():

            # Instantiate and return it;
            return model.nutrients.ReadonlyNutrientRatio(
                nutrient_name=nutrient_name,
                ratio_host=self,
                qty_ratio_data_src=lambda: self.nutrient_ratios_data[nutrient_name]
            )

        # Otherwise, return an error to indicate it isn't defined;
        else:
            raise model.nutrients.exceptions.UndefinedNutrientRatioError(
                subject=self,
                nutrient_name=nutrient_name
            )

    @property
    def nutrient_ratios_data(self) -> 'model.nutrients.NutrientRatiosData':
        """Returns the nutrient ratios data for the instance."""
        # First, find the common set of nutrients that are defined across all ingredients.
        defined_nutrient_sets = []

        # Create a list to cache the ingredients;
        ingredient_datafiles = []

        # Cycle through each ingredient;
        for idf_name in self.ingredient_quantities_data.keys():
            # Grab the datafile;
            idf = persistence.load_datafile(cls=model.ingredients.IngredientBase, datafile_name=idf_name)

            # Append it;
            ingredient_datafiles.append(idf)

            # Add its defined nutrients to the set list;
            defined_nutrient_sets.append(set(idf['nutrient_ratios_data'].keys()))

        # Grab the intersection of defined nutrient sets;
        common_nutrients = set.intersection(*defined_nutrient_sets)

        # Create somewhere to put the nutrient ratios;
        nutrient_ratios = {}

        # For each common nutrient, average across each ingredient;
        for nutrient_name in common_nutrients:
            nut_total = 0
            for idf in ingredient_datafiles:
                nut_total += idf['nutrient_ratios_data'][nutrient_name]['subject_qty_data']['quantity_in_g'] / \
                             idf['nutrient_ratios_data'][nutrient_name]['host_qty_data']['quantity_in_g']
            nutrient_ratios[nutrient_name] = model.quantity.QuantityRatioData(
                subject_qty_data=model.quantity.QuantityData(
                    quantity_in_g=nut_total / len(ingredient_datafiles),
                    pref_unit='g'
                ),
                host_qty_data=model.quantity.QuantityData(
                    quantity_in_g=1,
                    pref_unit='g'
                )
            )

        # Return
        return nutrient_ratios

    @property
    def typical_serving_size_g(self) -> float:
        """Returns the typical serving size associated with this recipe."""
        total_mass = 0
        for ingredient_qty_data in self.ingredient_quantities_data.values():
            total_mass += ingredient_qty_data['quantity_in_g']
        return total_mass

    @staticmethod
    def get_path_into_db() -> str:
        """Returns the directory name in the database."""
        return f"{persistence.configs.path_into_db}/recipes"

    @property
    def persistable_data(self) -> Dict[str, Any]:
        """Returns the persistable data for the recipe instance."""
        return super().persistable_data


class ReadonlyRecipe(
    RecipeBase,
):
    """Models a readable recipe."""

    def __init__(self, recipe_data_src: Callable[[], 'model.recipes.RecipeData'], **kwargs):
        super().__init__(**kwargs)

        # Stash the data src function;
        self._recipe_data_src = recipe_data_src

        # Populate the datafile name;
        self._datafile_name = model.recipes.get_datafile_name_for_unique_value(
            unique_value=self._recipe_data_src()['name']
        )

    @property
    def _name(self) -> Optional[str]:
        """Returns the Recipe name."""
        return self._recipe_data_src()['name']

    @property
    def ingredient_quantities_data(self) -> 'model.ingredients.IngredientQuantitiesData':
        """Returns the ingredient quantities data for the instance."""
        return self._recipe_data_src()['ingredient_quantities_data']

    @property
    def serve_intervals_data(self) -> List[str]:
        """Returns the serve times data for the instance."""
        return self._recipe_data_src()['serve_intervals']

    @property
    def instruction_src(self) -> str:
        """Returns the instruction source for the recipe."""
        return self._recipe_data_src()['instruction_src']

    @property
    def tags(self) -> List[str]:
        """Returns the tags associated with the recipe."""
        return self._recipe_data_src()['tags']


class SettableRecipe(
    RecipeBase,
    model.HasSettableName,
    model.ingredients.HasSettableIngredientQuantities,
    model.time.HasSettableServeIntervals,
    model.instructions.HasSettableInstructionSrc,
    model.tags.HasSettableTags,
    persistence.CanLoadData
):
    """Models a settable recipe."""

    def __init__(self, recipe_data: Optional['model.recipes.RecipeData'] = None, **kwargs):
        super().__init__(**kwargs)

        if recipe_data is not None:
            super().load_data(recipe_data)

            # Populate the datafile name;
            self._datafile_name = persistence.get_datafile_name_for_unique_value(
                cls=model.recipes.RecipeBase,
                unique_value=self.name
            )

    @model.HasReadableName.name.setter
    def name(self, name: Optional[str]) -> None:
        """Sets the name if unique to the recipe class, otherwise raises an exception."""
        # If the name is None, just set it and return;
        if name is None:
            self._name_ = name
            return

        # OK, the name isn't None, so we need to check if it is available;
        if persistence.check_unique_value_available(
                cls=self.__class__,
                proposed_value=name,
                ignore_datafile=self.datafile_name if self.datafile_name_is_defined else None
        ):
            # It is available, go ahead and set it;
            self._name_ = name

        # Otherwise, raise an exception;
        else:
            raise persistence.exceptions.UniqueValueDuplicatedError(duplicated_value=name)

    def load_data(self, data: 'model.recipes.RecipeData') -> None:
        """Loads data into the isntance."""
        super().load_data(data)
