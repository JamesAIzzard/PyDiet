import abc
from typing import Dict, Optional, Any

import model
import persistence


class CostData(model.quantity.RefQtyData):
    cost_per_g: Optional[float]


class SupportsCost(model.quantity.HasBulk, persistence.YieldsPersistableData, abc.ABC):
    """Base class for objects which support a readonly cost per quantity.
    Notes:
        Some subclasses won't store the cost per gram or preferred cost unit
        on the instance, so we require a couple of abstract methods to be implemented
        to get hold of this information.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    @abc.abstractmethod
    def _cost_data(self) -> 'CostData':
        """Returns the cost data for the instance."""
        raise NotImplementedError

    @property
    def cost_per_g(self) -> float:
        """Returns the cost of a single gram of the subject."""
        if self._cost_data['cost_per_g'] is None:
            raise model.cost.exceptions.UndefinedCostError(subject=self)
        return self._cost_data['cost_per_g']

    @property
    def cost_pref_unit(self) -> str:
        """Returns the preferred subject quantity unit to use when referring to cost.
        If this isn't configured on the subject, we fall back to the bulk pref unit.
        """
        if self.units_are_configured(self._cost_data['pref_unit']):
            return self._cost_data['pref_unit']
        else:
            return self.pref_unit

    @property
    def cost_ref_qty(self) -> float:
        """Returns the preferred subject quantity to use when referring to cost.
        If the cost pref unit isn't configured on the subject, we return the bulk ref qty instead.
        """
        if self.units_are_configured(self._cost_data['pref_unit']):
            return self._cost_data['ref_qty']
        else:
            return self.ref_qty

    @property
    def cost_per_pref_unit(self) -> float:
        """Returns the cost of one of the instance's preferred units."""
        # How many grams in one pref unit?
        g_per_pref_unit = model.quantity.convert_qty_unit(
            qty=1,
            start_unit=self.cost_pref_unit,
            end_unit='g',
            g_per_ml=self.g_per_ml if self.density_is_defined else None,
            piece_mass_g=self.piece_mass_g if self.piece_mass_defined else None
        )
        return g_per_pref_unit * self.cost_per_g

    @property
    def cost_of_ref_qty(self) -> float:
        return self.cost_per_pref_unit * self.cost_ref_qty

    @property
    def persistable_data(self) -> Dict[str, Any]:
        data = super().persistable_data
        # Correct the cost pref unit if it isn't defined;
        if not self.units_are_configured(self._cost_data['pref_unit']):
            data['cost_data'] = CostData(
                pref_unit=self.pref_unit,
                ref_qty=self.ref_qty,
                cost_per_g=self._cost_data['cost_per_g']
            )
        else:
            # No corrections required, just dump the data in;
            data['cost_data'] = self._cost_data
        return data


class SupportsSettableCost(SupportsCost, persistence.CanLoadData):
    """ABC for objects supporting settable abstract cost (costs per qty)."""

    def __init__(self, cost_data: Optional['CostData'] = None, **kwargs):
        super().__init__(**kwargs)

        self._cost_data_ = CostData(
            pref_unit='g',
            ref_qty=100,
            cost_per_g=None
        )

        if cost_data is not None:
            self.load_data({'cost_data': cost_data})

    @property
    def _cost_data(self) -> 'CostData':
        return self._cost_data_

    @SupportsCost.cost_per_g.setter
    def cost_per_g(self, cost_per_g: Optional[float]) -> None:
        """Validates and sets cost_per_g"""
        try:
            if cost_per_g is None:
                self._cost_data_['cost_per_g'] = None
            else:
                self._cost_data_['cost_per_g'] = model.cost.validation.validate_cost(cost_per_g)
        # OK, the cost wasn't valid, so attach a reference for this instance to the error object.
        except model.cost.exceptions.InvalidCostError as err:
            err.subject = self
            raise err

    @SupportsCost.cost_ref_qty.setter
    def cost_ref_qty(self, ref_qty: float) -> None:
        """Validates and sets the reference quantity associated with the cost."""
        self._cost_data['ref_qty'] = model.quantity.validation.validate_nonzero_quantity(ref_qty)

    @SupportsCost.cost_pref_unit.setter
    def cost_pref_unit(self, pref_unit: str) -> None:
        """Validates and sets the reference unit associated with the cost."""
        if self.units_are_configured(pref_unit):
            self._cost_data['pref_unit'] = pref_unit
        else:
            if model.quantity.units_are_volumes(pref_unit):
                raise model.quantity.exceptions.UndefinedDensityError(subject=self)
            elif model.quantity.units_are_pieces(pref_unit):
                raise model.quantity.exceptions.UndefinedPcMassError(subject=self)

    def set_cost(self, cost_gbp: Optional[float], qty: Optional[float], unit: str) -> None:
        """Sets the cost in gbp of any quanitity of any unit."""
        # If either of the values are None, just set to None;
        if qty is None or cost_gbp is None:
            self.cost_per_g = None
            return

        # Validate both values;
        cost_gbp = model.cost.validation.validate_cost(cost_gbp)
        qty = model.quantity.validation.validate_nonzero_quantity(qty)

        # Find the ratio of cost per original unit
        r = cost_gbp / qty

        # Convert ratio to grams
        k = model.quantity.convert_qty_unit(
            qty=1,
            start_unit=unit,
            end_unit='g',
            g_per_ml=self.g_per_ml if self.density_is_defined else None,
            piece_mass_g=self.g_per_ml if self.density_is_defined else None
        )

        # Calculate the final ratio;
        cost_per_g = r / k

        # Set the value;
        self.cost_per_g = cost_per_g
        self.cost_ref_qty = qty
        self.cost_pref_unit = unit

    def load_data(self, data: Dict[str, Any]) -> None:
        super().load_data(data)
        self._cost_data_ = data['cost_data']
