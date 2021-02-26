import abc
from typing import Dict, List, Optional

from model import quantity, ingredients


class IngredientAmount(quantity.HasQuantity):
    """Models a toleranced quantity of an ingredient."""

    def __init__(self, ingredient: 'ingredients.Ingredient', **kwargs):
        super().__init__(**kwargs)
        self._ingredient = ingredient


class HasIngredientAmounts(quantity.HasBulk, abc.ABC):
    """Models an object which has readonly ingredient amounts."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._ingredient_amounts: Dict[str, 'ingredients.IngredientAmount'] = {}

    @property
    def ingredient_amounts(self) -> Dict[str, 'ingredients.IngredientAmount']:
        # todo - This might need to be readonly?
        # Are there any instances where we might want to return IngredientAmount instances
        # that are immutable? For example on a meal? Perhaps the optimisation engine adjusts
        # recipes, and the resulting meals are immutable?
        raise NotImplementedError

    @property
    def ingredient_names(self) -> List[str]:
        """Returns a list of all the ingredients associated with the instance."""
        return list(self._ingredient_amounts.keys())


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
