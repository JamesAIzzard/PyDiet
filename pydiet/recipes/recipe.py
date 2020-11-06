from typing import Dict, List, Optional, TypedDict, TYPE_CHECKING

from pydiet import persistence, completion, flags, nutrients, quantity, ingredients, tags, time, steps, recipes
from pydiet.ingredients import Ingredient
from pydiet.quantity import BulkData, get_empty_bulk_data

if TYPE_CHECKING:
    from pydiet.persistence.supports_persistence import DBInfo, PersistenceInfo
    from pydiet.ingredients import IngredientAmountData
    from pydiet.nutrients import NutrientData


class RecipeData(TypedDict):
    name: Optional[str]
    ingredient_amounts: Dict[str, 'IngredientAmountData']
    bulk_data: BulkData
    serve_intervals: List[str]
    steps: Dict[int, str]
    tags: List[str]


def get_empty_recipe_data() -> RecipeData:
    return RecipeData(
        name=None,
        ingredient_amounts={},
        bulk_data=get_empty_bulk_data(),
        serve_intervals=[],
        steps={},
        tags=[]
    )


def get_new_recipe() -> 'Recipe':
    return Recipe(get_empty_recipe_data())


class Recipe(persistence.supports_persistence.SupportsPersistence,
             completion.has_mandatory_attributes.SupportsCompletion,
             flags.supports_flags.SupportsFlags,
             nutrients.supports_nutrient_content.SupportsNutrientContent,
             quantity.supports_bulk.SupportsBulk,
             ingredients.HasSettableIngredientAmounts,
             tags.supports_tags.SupportsSettingTags,
             time.supports_serve_times.SupportsSettingServeTimes,
             steps.supports_steps.SupportsSettingSteps):

    def __init__(self, data: 'RecipeData', datafile_name: Optional[str] = None):
        self._data = data
        self._datafile_name = datafile_name

    @property
    def missing_mandatory_attrs(self) -> List[str]:
        attr_names = []
        if not self.name_is_defined:
            attr_names.append('name')
        if len(self.ingredient_amounts_data) == 0:
            attr_names.append('ingredients')
        if len(self.tag_data) == 0:
            attr_names.append('tags')
        if len(self.serve_times_data) == 0:
            attr_names.append('serve_times')
        return attr_names

    @property
    def name(self) -> Optional[str]:
        return self._data['name']

    @name.setter
    def name(self, value: str) -> None:
        if persistence.core.check_unique_val_avail(recipes.Recipe, self.datafile_name, value):
            self._data['name'] = value
        else:
            raise persistence.exceptions.NameDuplicatedError('There is already a recipe called {}'.format(value))

    @property
    def name_is_defined(self) -> bool:
        return self.name is not None

    @property
    def _ingredient_amounts_data(self) -> Dict[str, 'IngredientAmountData']:
        return self._data['ingredient_amounts']

    @property
    def _flags_data(self) -> Dict[str, Optional[bool]]:
        # Assume a flag is true until we find a false or None;
        flags_data = flags.supports_flags.get_empty_flags_data()
        for flag_name in flags_data:
            flags_data[flag_name] = True
            for ingredient_df_name in self.ingredient_amounts_data:
                i_name = persistence.get_unique_val_from_df_name(Ingredient, ingredient_df_name)
                i = persistence.load(Ingredient, i_name)
                if i.get_flag_value(flag_name) is False:
                    flags_data[flag_name] = False
                    continue
                elif i.get_flag_value(flag_name) is None:
                    flags_data[flag_name] = None
                    continue
        return flags_data

    @property
    def _nutrients_data(self) -> Dict[str, 'NutrientData']:
        # Initialise the Dict for returning;
        nutrients_data: Dict[str, 'NutrientData'] = {}

        for nutrient_name in nutrients.all_primary_nutrient_names:
            # Initialise the nutrient;
            nutrients_data[nutrient_name] = NutrientData(
                nutrient_g_per_subject_g=None,
                nutrient_pref_units='g'
            )
            # Loop through all ingredient amounts, compiling qty. If any ingredient amounts have None against
            # this nutrient, the whole nutrient is reset to None, and we move onto the next nutrient;
            for ingredient_df_name in self.ingredient_amounts_data:
                i_name = persistence.get_unique_val_from_df_name(Ingredient, ingredient_df_name)
                i = persistence.load(Ingredient, i_name)
                g_current = i.nutrient_g_per_subject_g(nutrient_name)
                g_total = nutrients_data[nutrient_name]['nutrient_g_per_subject_g']
                if g_current is not None and g_total is None:
                    nutrients_data[nutrient_name]['nutrient_g_per_subject_g'] = g_current
                elif g_current is not None:
                    nutrients_data[nutrient_name]['nutrient_g_per_subject_g'] = g_current + g_total
                elif g_current is None:
                    nutrients_data[nutrient_name]['nutrient_g_per_subject_g'] = None
                    break
        return nutrients_data

    @property
    def bulk_data(self) -> 'BulkData':
        return self._data['bulk_data']

    @property
    def _tag_data(self) -> List[str]:
        return self._data['tags']

    @property
    def _serve_times_data(self) -> List[str]:
        return self._data['serve_intervals']

    @property
    def _persistence_info(self) -> 'PersistenceInfo':
        return persistence.supports_persistence.PersistenceInfo(
            data=self._data,
            datafile_name=self._datafile_name
        )

    @staticmethod
    def get_db_info() -> 'DBInfo':
        return persistence.supports_persistence.DBInfo(
            unique_field_name='name',
            path_into_db=persistence.configs.recipe_db_path
        )

    def set_datafile_name(self, datafile_name: str) -> None:
        self._datafile_name = datafile_name
