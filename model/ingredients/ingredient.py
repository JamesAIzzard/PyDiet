from typing import Optional, Dict, List, TypedDict

import model
import persistence


class IngredientData(TypedDict):
    """Ingredient data dictionary."""
    cost_per_g: Optional[float]
    flags: Dict[str, Optional[bool]]
    name: Optional[str]
    nutrients: Dict[str, 'model.nutrients.NutrientRatioData']
    bulk: model.quantity.BulkData


class Ingredient(
    persistence.SupportsPersistence,
    model.HasName,
    model.HasMandatoryAttributes,
    model.cost.SupportsCostPerQuantity,
    model.flags.HasFlags,
    model.nutrients.HasNutrientRatios
):
    def __init__(self, ingredient_data: Optional['IngredientData'] = None, **kwargs):
        super().__init__(**kwargs)


class SettableIngredient(persistence.SupportsPersistence,
                         model.HasSettableName,
                         model.HasMandatoryAttributes,
                         model.quantity.HasSettableBulk,
                         model.cost.SupportsSettableCostPerQuantity,
                         model.flags.HasSettableFlags,
                         model.nutrients.HasSettableNutrientRatios):

    def __init__(self, ingredient_data: Optional[IngredientData] = None, **kwargs):
        super().__init__(**kwargs)

        # Load any data that was provided;
        if ingredient_data is not None:
            self.load_data(ingredient_data)

    @model.HasSettableName.name.setter
    def name(self, name: Optional[str]) -> None:
        # Extend the base implementation to check name uniqueness, since it is the index key;
        if persistence.check_unique_value_available(
                cls=Ingredient,
                proposed_name=name,
                ignore_datafile=self.datafile_name if self.datafile_name_is_defined else None
        ):
            self._name = name
        else:
            raise persistence.exceptions.UniqueValueDuplicatedError(
                subject=self,
                duplicated_value=name
            )

    @property
    def unique_value(self) -> str:
        # We are using the name as the unique value here;
        try:
            return self.name
        # If we get an undefined name error, convert it to an undefined unique value error.
        except model.exceptions.UndefinedNameError:
            raise persistence.exceptions.UndefinedUniqueValueError(subject=self)

    @property
    def missing_mandatory_attrs(self) -> List[str]:
        missing_attr_names = []
        # Check name;
        if self._name is None:
            missing_attr_names.append('name')
        # Check cost;
        if self._cost_per_g is None:
            missing_attr_names.append('cost')
        # Check flag_data;
        for flag_name in self.get_undefined_flag_names():
            missing_attr_names.append(f"{flag_name.replace('_', ' ')} flag")
        # Check nutrients;
        missing_attr_names = missing_attr_names + self.undefined_mandatory_nutrient_ratios
        return missing_attr_names

    @staticmethod
    def get_path_into_db() -> str:
        return persistence.configs.path_into_db + 'ingredients/'

    @property
    def persistable_data(self) -> Dict[str, IngredientData]:
        return super().persistable_data

    def load_data(self, data: 'IngredientData') -> None:
        super().load_data(data)
