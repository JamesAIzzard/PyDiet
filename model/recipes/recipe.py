from typing import Dict, List, TypedDict, Optional

from model import nutrients, ingredients, quantity, flags, persistence, mandatory_attributes, tags, time, steps


class RecipeData(TypedDict):
    """Recipe data dictionary."""
    name: Optional[str]
    # ingredient_amounts: Dict[str, 'IngredientAmountData']
    bulk_data: quantity.BulkData
    serve_intervals: List[str]
    steps: Dict[int, str]
    tags: List[str]


class Recipe(persistence.SupportsPersistence,
             mandatory_attributes.HasMandatoryAttributes,
             flags.HasFlags,
             nutrients.HasNutrientRatios,
             quantity.HasSettableBulk,
             # ingredients.HasSettableIngredientAmounts,
             # tags.supports_tags.HasSettableTags,
             # time.supports_serve_times.HasSettableServeTimes,
             # steps.supports_steps.HasSettableSteps
             ):
    """Models a recipe. A recipe is a mutable collection of ingredient ratios, which also supports
    tagging (meal, dessert, drink, etc), serve times, and steps.
    """

    def __init__(self, recipe_data: Optional['RecipeData'] = None, **kwargs):
        super().__init__(**kwargs)
        # Load any recipe data that was provided;
        if recipe_data is not None:
            self.load_data(recipe_data)

    @property
    def missing_mandatory_attrs(self) -> List[str]:
        attr_names = []
        # if not self.name_is_defined:
        #     attr_names.append('name')
        # if len(self.ingredient_amounts_data) == 0:
        #     attr_names.append('ingredients')
        # if len(self.tag_data) == 0:
        #     attr_names.append('tags')
        # if len(self.serve_times_data) == 0:
        #     attr_names.append('serve_times')
        return attr_names

    def _density_reset_cleanup(self) -> None:
        pass

    def _piece_mass_reset_cleanup(self) -> None:
        pass

    @property
    def name(self) -> Optional[str]:
        """Returns the name, which is also the unique value of a recipe."""
        return self.get_unique_value()

    @name.setter
    def name(self, name: Optional[str]) -> None:
        """Setter for the name. Ensures the name is unique before setting."""
        self.set_unique_value(name)

    @property
    def name_is_defined(self) -> bool:
        """Returns True/False to indicate if the ingredient name has been defined."""
        return self.unique_value_defined

    @staticmethod
    def get_path_into_db() -> str:
        return persistence.configs.recipe_db_path

    def persistable_data(self) -> Dict[str, 'RecipeData']:
        return RecipeData()

    def load_data(self, data: Dict[str, 'RecipeData']) -> None:
        raise NotImplementedError
