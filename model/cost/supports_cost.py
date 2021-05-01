import abc
from typing import Dict, Optional, Any

import model
import persistence


class SupportsCost(model.quantity.HasBulk, persistence.HasPersistableData, abc.ABC):
    """ABC for objects supporting abstract cost (costs per qty)."""

    def __init__(self, cost_per_g: Optional[float] = None, **kwargs):
        super().__init__(**kwargs)

        self._cost_per_g: Optional[float] = None

        if cost_per_g is not None:
            self.load_data(data={'cost_per_g': cost_per_g})

    @property
    def cost_per_g(self) -> float:
        """Returns the cost of a single gram of the subject."""
        if self._cost_per_g is None:
            raise model.cost.exceptions.UndefinedCostError(subject=self)
        return self._cost_per_g

    @property
    def cost_per_pref_unit(self) -> float:
        """Returns the cost of one of the instance's preferred units."""
        return model.quantity.convert_qty_unit(
            qty=self.cost_per_g,
            start_unit=self.pref_unit,
            end_unit='g',
            g_per_ml=self.g_per_ml if self.density_is_defined else None,
            piece_mass_g=self.piece_mass_g if self.density_is_defined else None
        )

    @property
    def cost_of_ref_qty(self) -> float:
        return self.cost_per_pref_unit * self.ref_qty

    @property
    def persistable_data(self) -> Dict[str, Any]:
        data = super().persistable_data
        data['cost_per_g'] = self._cost_per_g
        return data

    def load_data(self, data: Dict[str, Any]) -> None:
        super().load_data(data)
        self._cost_per_g = data['cost_per_g']


class SupportsSettableCost(SupportsCost, abc.ABC):
    """ABC for objects supporting settable abstract cost (costs per qty)."""

    @SupportsCost.cost_per_g.setter
    def cost_per_g(self, cost_per_g: Optional[float]) -> None:
        """Validates and sets cost_per_g"""
        if cost_per_g is None:
            self._cost_per_g = None
        else:
            self._cost_per_g = model.cost.validation.validate_cost(cost_per_g)

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
