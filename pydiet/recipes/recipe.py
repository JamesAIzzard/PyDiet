from typing import Dict, List, Optional, TypedDict, TYPE_CHECKING

from pydiet import persistence, completion, flags, nutrients, quantity, ingredients, tags, time, steps

if TYPE_CHECKING:
    from pydiet.persistence.supports_persistence import DBInfo, PersistenceInfo


class RecipeData(TypedDict):
    name: Optional[str]
    ingredient_composition: Dict[str, 'IngredientCompositionData']
    serve_intervals: List[str]
    steps: Dict[int, str]
    tags: List[str]


def get_empty_recipe_data() -> RecipeData:
    return RecipeData(
        name=None,
        ingredient_composition={},
        serve_intervals=[],
        steps={},
        tags=[]
    )


def get_new_recipe() -> 'Recipe':
    return Recipe(get_empty_recipe_data())


class Recipe(persistence.supports_persistence.SupportsPersistence,
             completion.supports_completion.SupportsCompletion,
             flags.supports_flags.SupportsFlags,
             nutrients.supports_nutrient_content.SupportsNutrientContent,
             quantity.supports_bulk.SupportsBulk,
             ingredients.supports_ingredient_composition.SupportsSettingIngredientComposition,
             tags.supports_tags.SupportsSettingTags,
             time.supports_serve_times.SupportsSettingServeTimes,
             steps.supports_steps.SupportsSettingSteps):

    def __init__(self, data: 'RecipeData', datafile_name: Optional[str] = None):
        self._data = data
        self._datafile_name = datafile_name
        self._name: Optional[str] = None

    @property
    def _flags_data(self) -> Dict[str, Optional[bool]]:
        flags_data = flags.supports_flags.get_empty_flags_data()
        for flag_name in flags_data:
            flags_data[flag_name] = True
            for ic in self._ingredient_composition:
                if ic.ingredient.get_flag_value(flag_name) is False:
                    flags_data[flag_name] = False
                    continue
                elif ic.ingredient.get_flag_value(flag_name) is None:
                    flags_data[flag_name] = None
        return flags_data

    @property
    def _ingredient_composition(self) -> Dict[str, 'IngredientPercentageData']:
        ...

    @property
    def _nutrients_data(self) -> Dict[str, 'NutrientData']:
        ...

    @property
    def missing_mandatory_attrs(self) -> List[str]:
        attr_names = []
        if not self.name_is_defined:
            attr_names.append('name')
        if len(self.ingredients) == 0:
            attr_names.append('ingredients')
        if len(self.tags) == 0:
            attr_names.append('tags')
        if len(self.serve_times) == 0:
            attr_names.append('serve_times')
        return attr_names

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def name_is_defined(self) -> bool:
        return self.name is None

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

    def set_name(self, value: str) -> None:
        self.set_unique_field(value)
