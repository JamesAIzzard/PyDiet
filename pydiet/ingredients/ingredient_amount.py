import abc
import copy
from typing import Dict, List, TypedDict, Optional, TYPE_CHECKING

import pydiet
from pydiet import ingredients, quantity, persistence

if TYPE_CHECKING:
    from pydiet.ingredients import Ingredient


class IngredientAmountData(TypedDict):
    quantity_g: Optional[float]
    pref_quantity_unit: str
    perc_increase: float
    perc_decrease: float


def get_new_ingredient_amount_data() -> 'IngredientAmountData':
    """Returns a new instance of IngredientAmountData."""
    return IngredientAmountData(quantity_g=None,
                                pref_quantity_unit='g',
                                perc_increase=0,
                                perc_decrease=0)


def ingredient_amount_data_defined(ingredient_amount_data: 'IngredientAmountData') -> bool:
    """Inspects an instance of IngredientAmountData and returns True/False to indicate if
    it is fully defined."""
    return None not in ingredient_amount_data.values()


def summarise_ingredient_amount_data(ingredient_amount_data: 'IngredientAmountData', ingredient: 'Ingredient') -> str:
    if not ingredient_amount_data_defined(ingredient_amount_data):
        return 'Undefined'
    template = '{qty}{unit} (+{inc}%/-{dec}%)'
    return template.format(
        qty=quantity.quantity_service.convert_qty_unit(
            qty=ingredient_amount_data['quantity_g'],
            start_unit='g',
            end_unit=ingredient_amount_data['pref_quantity_unit'],
            g_per_ml=ingredient_g_per_ml,
            piece_mass_g=ingredient_piece_mass_g
        ),
        unit=ingredient_amount_data['pref_quantity_unit'],
        inc=ingredient_amount_data['perc_increase'],
        dec=ingredient_amount_data['perc_decrease']
    )


class HasIngredientAmounts(abc.ABC):
    """Models an object which has readonly ingredient amounts."""

    @property
    @abc.abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def _ingredient_amounts_data(self) -> Dict[str, 'IngredientAmountData']:
        raise NotImplementedError

    @property
    def ingredient_amounts_data(self) -> Dict[str, 'IngredientAmountData']:
        return copy.deepcopy(self._ingredient_amounts_data)

    @property
    def ingredient_amounts_summary(self) -> str:
        summary = ''
        if len(self.ingredient_amounts_data):
            for df_name, data in self.ingredient_amounts_data.items():
                summary = summary + '\n' + self.summarise_ingredient_amount(df_name)
        else:
            summary = 'No ingredients to show yet.'
        return summary

    @property
    def ingredient_names(self) -> List[str]:
        names = []
        for ing_df_name in self.ingredient_amounts_data:
            name = ingredients.get_ingredient_name(ing_df_name)
            names.append(name)
        return names

    def get_ingredient_amount_data(self,
                                   df_name: Optional[str] = None,
                                   ingredient_name: Optional[str] = None) -> 'IngredientAmountData':
        if ingredient_name is not None:
            df_name = persistence.get_df_name_from_unique_val(ingredients.Ingredient, ingredient_name)
        return self.ingredient_amounts_data[df_name]

    def get_ingredient_amount_qty_g(self, df_name: str) -> Optional[float]:
        iad = self.get_ingredient_amount_data(df_name)
        return iad['quantity_g']

    def get_ingredient_amount_pref_unit(self, df_name: str) -> str:
        iad = self.get_ingredient_amount_data(df_name)
        return iad['pref_quantity_unit']

    def get_ingredient_amount_in_pref_units(self, df_name: str) -> float:
        iad = self.get_ingredient_amount_data(df_name)
        i_name = persistence.get_unique_val_from_df_name(df_name)
        i = persistence.load(ingredients.Ingredient, i_name)
        return quantity.quantity_service.convert_qty_unit(
            qty=iad['quantity_g'],
            start_unit='g',
            end_unit=iad['pref_quantity_unit'],
            g_per_ml=i.g_per_ml,
            piece_mass_g=i.piece_mass_g
        )

    def get_ingredient_amount_perc_incr(self, df_name: str) -> float:
        iad = self.get_ingredient_amount_data(df_name)
        return iad['perc_increase']

    def get_ingredient_amount_perc_decr(self, df_name: str) -> float:
        iad = self.get_ingredient_amount_data(df_name)
        return iad['perc_decrease']

    def ingredient_amount_defined(self, df_name: str) -> bool:
        iad = self.get_ingredient_amount_data(df_name)
        return ingredient_amount_data_defined(iad)

    def summarise_ingredient_amount(self, df_name: str) -> str:
        ingredient_name = persistence.get_unique_val_from_df_name(ingredients.Ingredient, df_name)
        i = persistence.load(ingredients.Ingredient, ingredient_name)
        return summarise_ingredient_amount(self.get_ingredient_amount_data(df_name=df_name))


class HasSettableIngredientAmounts(HasIngredientAmounts, abc.ABC):
    """Models an object which has settable ingredient amounts."""

    @property
    def ingredient_amounts_data(self) -> Dict[str, 'IngredientAmountData']:
        return self._ingredient_amounts_data

    def add_new_ingredient_amount(self, ingredient_df_name: str) -> None:
        self.ingredient_amounts_data[ingredient_df_name] = get_new_ingredient_amount_data()

    def set_ingredient_amount_qty(self, df_name: str, amount: Optional[float]) -> None:
        amount = quantity.validate_quantity(amount)
        self.get_ingredient_amount_data(df_name)['quantity'] = amount

    def set_ingredient_amount_unit(self, df_name: str, unit: str) -> None:
        i_name = persistence.get_unique_val_from_df_name(ingredients.Ingredient, df_name)
        i = persistence.load(ingredients.Ingredient, i_name)
        if i.check_units_configured(unit):
            self.get_ingredient_amount_data(df_name)['quantity_unit'] = unit
        else:
            raise quantity.exceptions.UnitNotConfiguredError

    def set_ingredient_amount_perc_incr(self, df_name: str, perc_incr: float) -> None:
        if perc_incr < 0:
            raise pydiet.exceptions.InvalidPositivePercentageError
        self.get_ingredient_amount_data(df_name)['perc_increase'] = perc_incr

    def set_ingredient_amount_perc_decr(self, df_name: str, perc_decr: float) -> None:
        if perc_decr < 0:
            raise pydiet.exceptions.InvalidPositivePercentageError
        self.get_ingredient_amount_data(df_name)['perc_increase'] = perc_decr

    def set_ingredient_amount_data(self, data: 'IngredientAmountData', ingredient_name: Optional[str] = None,
                                   ingredient_df_name: Optional[str] = None):
        if ingredient_name is not None:
            ingredient_df_name = persistence.get_df_name_from_unique_val(ingredients.Ingredient, ingredient_name)
        if ingredient_df_name not in self.ingredient_amounts_data.keys():
            from pydiet import recipes
            raise recipes.exceptions.IngredientNotInRecipeError
        self.set_ingredient_amount_qty(ingredient_df_name, data['quantity'])
        self.set_ingredient_amount_unit(ingredient_df_name, data['quantity_unit'])
        self.set_ingredient_amount_perc_incr(ingredient_df_name, data['perc_increase'])
        self.set_ingredient_amount_perc_decr(ingredient_df_name, data['perc_decrease'])

    def set_ingredient_amounts_data(self, data: Dict[str, 'IngredientAmountData']):
        self.ingredient_amounts_data.clear()
        for df_name, ia_data in data.items():
            self.ingredient_amounts_data[df_name] = self.set_ingredient_amount_data(ia_data,
                                                                                    ingredient_df_name=df_name)

    def remove_ingredient_amount(self, ingredient_name: Optional[str] = None, ingredient_df_name: Optional[str] = None):
        if ingredient_name is not None:
            ingredient_df_name = persistence.get_df_name_from_unique_val(ingredients.Ingredient, ingredient_name)
        del self.ingredient_amounts_data[ingredient_df_name]
