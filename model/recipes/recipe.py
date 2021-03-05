from typing import Dict, List, TypedDict, Optional

from model import recipes, ingredients, quantity, persistence, mandatory_attributes


class RecipeData(TypedDict):
    """Recipe data dictionary."""
    name: Optional[str]
    # ingredient_amounts: Dict[str, 'IngredientAmountData']
    bulk_data: quantity.BulkData
    serve_intervals: List[str]
    steps: Dict[int, str]
    tags: List[str]


class Recipe(persistence.SupportsPersistence,
             mandatory_attributes.HasMandatoryAttributes):
    """Models a recipe. A recipe is a collection of ingredient ratios, which also supports
    tagging (meal, dessert, drink, etc), serve times, and steps.
    """

    def __init__(self, recipe_data: Optional['RecipeData'] = None, **kwargs):
        super().__init__(**kwargs)

        # Init the ingredient ratio dictionary;
        self._ingredient_ratios: Dict[str, 'recipes.RecipeIngredientRatio'] = {}

        # Load any recipe data that was provided;
        if recipe_data is not None:
            self.load_data(recipe_data)

    @property
    def missing_mandatory_attrs(self) -> List[str]:
        attr_names = []
        if not self.name_is_defined:
            attr_names.append('name')
        return attr_names

    def _density_reset_cleanup(self) -> None:
        pass

    def _piece_mass_reset_cleanup(self) -> None:
        pass

    @property
    def name(self) -> Optional[str]:
        """Returns the name, which is also the unique value of a recipe."""
        return self.unique_value

    @name.setter
    def name(self, name: Optional[str]) -> None:
        """Setter for the name. Ensures the name is unique before setting."""
        self.unique_value = name

    @property
    def name_is_defined(self) -> bool:
        """Returns True/False to indicate if the ingredient name has been defined."""
        return self.unique_value_defined

    def add_ingredient_ratio(self, ingredient_name: Optional[str] = None,
                             ingredient_df_name: Optional[str] = None,
                             ingredient_nominal_quantity: Optional[float] = None,
                             quantity_units: Optional[str] = None,
                             inc_perc: Optional[float] = None,
                             dec_perc: Optional[float] = None) -> None:
        """Adds an ingredient ratio to the recipe."""
        # Check ingredient is identified;
        if ingredient_name is None and ingredient_df_name is None:
            raise ValueError('Ingredient name or datafile name must be specified.')

        # Grab the datafile name if we don't have it;
        if ingredient_df_name is None:
            ingredient_df_name = persistence.get_datafile_name_for_unique_value(ingredient_name)

        # Load the ingredient;
        ingredient = persistence.load(ingredients.Ingredient, ingredient_df_name)

        # Init the RecipeIngredientRatio;
        rir = recipes.RecipeIngredientRatio(ingredient=ingredient,
                                            recipe=self,
                                            nominal_quantity=ingredient_nominal_quantity,
                                            nominal_quantity_units=quantity_units,
                                            perc_incr=inc_perc,
                                            perc_decr=dec_perc)

        # Attach the instance to the dict;
        self._ingredient_ratios[ingredient_df_name] = rir

    @property
    def ingredient_names(self) -> List[str]:
        """Returns a list of all the unique ingredient names associated with this recipe instance."""
        names: List[str] = []
        for ingredient_df_name in self._ingredient_ratios.keys():
            names.append(persistence.get_unique_value_from_datafile_name(ingredient_df_name))
        return names

    def mutate(self) -> 'MealComponent':
        """Takes the current Recipe parameters and outputs a concrete MealComponent instance."""

    @staticmethod
    def get_path_into_db() -> str:
        return persistence.configs.recipe_db_path

    def persistable_data(self) -> Dict[str, 'RecipeData']:
        return RecipeData()

    def load_data(self, data: Dict[str, 'RecipeData']) -> None:
        raise NotImplementedError
