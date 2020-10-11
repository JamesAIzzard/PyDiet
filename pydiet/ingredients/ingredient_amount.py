import abc
from typing import List, Dict, Optional, TypedDict, TYPE_CHECKING

import pydiet
from pydiet import quantity
from pydiet.ingredients import Ingredient, IngredientData

if TYPE_CHECKING:
    from pydiet.ingredients import IngredientData


class IngredientAmountData(TypedDict):
    quantity: Optional[float]
    quantity_unit: Optional[str]
    perc_increase: Optional[float]
    perc_decrease: Optional[float]


class IngredientAmount(Ingredient):
    """Models an ingredient with immutable quantity and tolerance associated with it."""

    def __init__(self, ingredient_data: 'IngredientData',
                 ingredient_datafile_name: str,
                 ingredient_amount_data: 'IngredientAmountData'):
        super().__init__(data=ingredient_data, datafile_name=ingredient_datafile_name)
        self._data = ingredient_amount_data

    @property
    def missing_mandatory_attrs(self) -> List[str]:
        missing_attrs = super().missing_mandatory_attrs
        if not self.quantity_is_defined:
            missing_attrs.append('quantity')
        if not self.quantity_tolerance_is_defined:
            missing_attrs.append('quantity tolerance')
        return missing_attrs

    @property
    def quantity(self) -> Optional[float]:
        return self._data['quantity']

    @property
    def quantity_unit(self) -> Optional[str]:
        return self._data['quantity_unit']

    @property
    def quantity_is_defined(self) -> bool:
        if self.quantity is None or self.quantity_unit is None:
            return False
        else:
            return True

    @property
    def perc_increase(self) -> Optional[float]:
        return self._data['perc_increase']

    @property
    def perc_decrease(self) -> Optional[float]:
        return self._data['perc_decrease']

    @property
    def quantity_tolerance_is_defined(self) -> bool:
        if self.perc_increase is None or self.perc_decrease is None:
            return False
        else:
            return True

    @property
    def summary(self) -> str:
        summary = 'Undefined'
        if self.quantity_is_defined and self.quantity_tolerance_is_defined:
            summary = '{qty} (+{perc_inc:.1f}%/-{perc_dec:.1f}%)'.format(
                qty=str(self.quantity) + str(self.quantity_unit),
                perc_inc=self.perc_increase,
                perc_dec=self.perc_decrease
            )
        return summary


class SettableIngredientAmount(IngredientAmount):
    """Models and ingredient amount with mutable properties."""
    def __init__(self, ingredient_data: 'IngredientData',
                 ingredient_datafile_name: str,
                 ingredient_amount_data: 'IngredientAmountData'):
        super().__init__(ingredient_data, ingredient_datafile_name, ingredient_amount_data)

    @IngredientAmount.quantity.setter
    def quantity(self, value: Optional[float]) -> None:
        if value is not None:
            value = quantity.validate_quantity(value)
        self._data['quantity'] = value

    @IngredientAmount.quantity_unit.setter
    def quantity_unit(self, unit: Optional[str]) -> None:
        if unit is not None:
            self.check_units_configured(unit)
        self._data['quantity_unit'] = unit

    @IngredientAmount.perc_increase.setter
    def perc_increase(self, value: Optional[float]) -> None:
        if value is not None:
            pydiet.validation.validate_positive_percentage(value)
        self._data['perc_increase'] = value

    @IngredientAmount.perc_decrease.setter
    def perc_decrease(self, value: Optional[float]) -> None:
        if value is not None:
            pydiet.validation.validate_positive_percentage(value)
        self._data['perc_decrease'] = value


class HasIngredientAmounts(abc.ABC):
    """Models an object which has readonly ingredient amounts."""
    @property
    @abc.abstractmethod
    def ingredient_amounts(self) -> Dict[str, 'IngredientAmount']:
        raise NotImplementedError

    @property
    def ingredient_amounts_summary(self) -> str:
        summary = ''
        if len(self.ingredient_amounts):
            for ia in self.ingredient_amounts.values():
                summary = summary + '{ingredient_name}: {ci_summary}\n'.format(
                    ingredient_name=ia.name,
                    ci_summary=ia.summary
                )
        else:
            summary = 'No ingredients to show yet.'
        return summary


class HasSettableIngredientAmounts(HasIngredientAmounts, abc.ABC):
    """Models an object which has settable ingredient amounts."""
    @property
    @abc.abstractmethod
    def ingredient_amounts(self) -> Dict[str, 'SettableIngredientAmount']:
        raise NotImplementedError
