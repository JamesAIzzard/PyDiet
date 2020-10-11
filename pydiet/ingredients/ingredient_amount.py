import abc
import copy
from typing import Dict, TypedDict, Optional

import pydiet
from pydiet import quantity, persistence
from pydiet.ingredients import Ingredient


class IngredientAmountData(TypedDict):
    quantity: Optional[float]
    quantity_unit: str
    perc_increase: float
    perc_decrease: float


def get_new_ingredient_amount_data() -> 'IngredientAmountData':
    return IngredientAmountData(quantity=None,
                                quantity_unit='g',
                                perc_increase=0,
                                perc_decrease=0)


class HasIngredientAmounts(abc.ABC):
    """Models an object which has readonly ingredient amounts."""

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

    def get_ingredient_amount_data(self, df_name: str) -> 'IngredientAmountData':
        return self.ingredient_amounts_data[df_name]

    def get_ingredient_amount_qty(self, df_name: str) -> Optional[float]:
        iad = self.get_ingredient_amount_data(df_name)
        return iad['quantity']

    def get_ingredient_amount_unit(self, df_name: str) -> str:
        iad = self.get_ingredient_amount_data(df_name)
        return iad['quantity_unit']

    def get_ingredient_amount_perc_incr(self, df_name: str) -> float:
        iad = self.get_ingredient_amount_data(df_name)
        return iad['perc_increase']

    def get_ingredient_amount_perc_decr(self, df_name: str) -> float:
        iad = self.get_ingredient_amount_data(df_name)
        return iad['perc_increase']

    def ingredient_amount_defined(self, df_name: str) -> float:
        iad = self.get_ingredient_amount_data(df_name)
        return iad['quantity'] is None

    def summarise_ingredient_amount(self, df_name) -> str:
        if self.ingredient_amount_defined(df_name):
            return '{qty}{unit} (+{inc}%/-{dec}%)'.format(
                qty=self.get_ingredient_amount_data(df_name),
                unit=self.get_ingredient_amount_unit(df_name),
                inc=self.get_ingredient_amount_perc_incr(df_name),
                dec=self.get_ingredient_amount_perc_decr(df_name)
            )
        else:
            return 'Undefined'


class HasSettableIngredientAmounts(HasIngredientAmounts, abc.ABC):
    """Models an object which has settable ingredient amounts."""

    @property
    def ingredient_amounts_data(self) -> Dict[str, 'IngredientAmountData']:
        return self._ingredient_amounts_data

    def set_ingredient_amount_qty(self, df_name: str, amount: Optional[float]) -> None:
        amount = quantity.validate_quantity(amount)
        self.get_ingredient_amount_data(df_name)['quantity'] = amount

    def set_ingredient_amount_unit(self, df_name: str, unit: str) -> None:
        i_name = persistence.get_unique_val_from_df_name(Ingredient, df_name)
        i = persistence.load(Ingredient, i_name)
        if i.check_units_configured(unit):
            self.get_ingredient_amount_data(df_name)['quantity_unit'] = unit
        else:
            raise quantity.exceptions.UnitNotConfiguredError

    def set_ingredient_amount_perc_incr(self, df_name: str, perc_incr: float) -> None:
        if perc_incr < 0:
            raise pydiet.exceptions.InvalidPositivePercentageError
        self.get_ingredient_amount_data(df_name)['perc_increase'] = perc_incr

    def set_ingredient_amount_perc_inrc(self, df_name: str, perc_decr: float) -> None:
        if perc_decr < 0:
            raise pydiet.exceptions.InvalidPositivePercentageError
        self.get_ingredient_amount_data(df_name)['perc_increase'] = perc_decr
