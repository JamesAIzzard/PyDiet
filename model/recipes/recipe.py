from typing import Dict, List, TypedDict, Optional

import model
import persistence


class RecipeData(TypedDict):
    """Recipe data dictionary."""
    name: Optional[str]
    ingredient_amounts: Dict[str, 'model.ingredients.IngredientQuantityData']
    bulk_data: model.quantity.BulkData
    serve_intervals: List[str]
    instruction_src: str
    tags: List[str]


class Recipe(persistence.SupportsPersistence,
             model.HasSettableName,
             model.HasMandatoryAttributes,
             model.quantity.HasSettableBulk,
             model.cost.HasReadableCostPerQuantity,
             model.flags.HasReadableFlags,
             model.nutrients.HasReadableNutrientRatios,
             model.ingredients.HasSettableIngredientQuantities):

    def __init__(self, recipe_data: Optional['RecipeData'] = None, **kwargs):
        super().__init__(**kwargs)

        # Load any data that was provided;
        if recipe_data is not None:
            self.load_data(recipe_data)

    @staticmethod
    def get_path_into_db() -> str:
        return persistence.configs.ingredient_db_path

    @property
    def unique_value(self) -> str:
        # We are using the name as the unique value here;
        try:
            return self.name
        except model.exceptions.UndefinedNameError:
            raise persistence.exceptions.UndefinedUniqueValueError(subject=self)

    @property
    def missing_mandatory_attrs(self) -> List[str]:
        missing_attr_names = []
        if self._name is None:
            missing_attr_names.append('name')
        if len(self._ingredient_quantities) == 0:
            missing_attr_names.append('ingredients')
        return missing_attr_names

    @property
    def nutrient_ratios(self) -> Dict[str, 'model.nutrients.ReadonlyNutrientRatio']:
        raise NotImplementedError
        # # We need to average the ingredient ratios across the number of ingredients.
        # # First, create a dictionary to store rolling totals of each nutrient ratio;
        # nutrient_ratio_totals: Dict[str, float] = {}
        # for ingredient_df_name, ingredient_quantity in self.ingredient_quantities.values():
        #     for nutrient_name, nutrient_ratio in ingredient_
