"""Module providing cost per quantity functionality."""
import abc
from typing import Dict, Optional, Any

import model
import persistence


class HasReadableCostPerQuantity(persistence.YieldsPersistableData, abc.ABC):
    """Abstract class to implement functionality associated with a readable cost per quantity."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    @abc.abstractmethod
    def cost_per_qty_data(self) -> 'model.cost.CostPerQtyData':
        """Returns the cost data for the instance."""
        raise NotImplementedError

    @property
    def cost_is_defined(self) -> bool:
        """Returns True/False to indicate if the cost per qty is defined."""
        if self.cost_per_qty_data['cost_per_g'] is None:
            return False
        else:
            return True

    @property
    def cost_ref_subject_quantity(self) -> 'model.quantity.HasReadonlyQuantityOf':
        """Returns the subject quantity against which the cost is defined.
        Notes:
            Since the cost data is readonly here, we just generate a quantity
            object from the information in cost data. This allows us to
            leverage its unit manipulation methods elsewhere.
        """
        return model.quantity.HasReadonlyQuantityOf(
            qty_subject=self,
            quantity_data_src=lambda: model.quantity.QuantityData(
                quantity_in_g=self.cost_per_qty_data['quantity_in_g'],
                pref_unit=self.cost_per_qty_data['pref_unit']
            )
        )

    @property
    def cost_per_g(self) -> float:
        """Returns the cost of a single gram of the subject."""
        if self.cost_per_qty_data['cost_per_g'] is None:
            raise model.cost.exceptions.UndefinedCostError(subject=self)

        return self.cost_per_qty_data['cost_per_g']

    @property
    def cost_per_pref_unit(self) -> float:
        """Returns the cost of one of the instance's preferred units."""
        # How many grams in one pref unit?
        g_per_ml = None
        piece_mass_g = None
        if isinstance(self, model.quantity.HasReadableExtendedUnits):
            g_per_ml = self.g_per_ml if self.density_is_defined else None
            piece_mass_g = self.piece_mass_g if self.piece_mass_is_defined else None
        g_per_pref_unit = model.quantity.convert_qty_unit(
            qty=1,
            start_unit=self.cost_ref_subject_quantity.pref_unit,
            end_unit='g',
            g_per_ml=g_per_ml,
            piece_mass_g=piece_mass_g
        )
        # Multiply that out and return;
        return g_per_pref_unit * self.cost_per_g

    @property
    def cost_of_ref_qty(self) -> float:
        """Returns the cost and reference quantity used for definition."""
        return self.cost_per_pref_unit * self.cost_ref_subject_quantity.ref_qty

    @property
    def persistable_data(self) -> Dict[str, Any]:
        """Returns the persistable data dict, updated with the cost data."""
        data = super().persistable_data
        data['cost_per_qty_data'] = self.cost_per_qty_data
        return data


class HasSettableCostPerQuantity(HasReadableCostPerQuantity, persistence.CanLoadData):
    """Class to implement functionality associated with a settable cost per quantity."""

    def __init__(self, cost_per_qty_data: Optional['model.cost.CostPerQtyData'] = None, **kwargs):
        super().__init__(**kwargs)

        # Create vars to store the data locally now;
        # Create a subject quantity instance;
        self._cost_ref_qty = model.quantity.HasSettableQuantityOf(
            qty_subject=self,
            quantity_data=model.quantity.QuantityData(
                quantity_in_g=None,
                pref_unit='g'
            )
        )
        # Create somewhere to put the cost per gram value;
        self._cost_per_g_: Optional[float] = None

        # If we got data, load it;
        if cost_per_qty_data is not None:
            self.load_data({'cost_per_qty_data': cost_per_qty_data})

    @property
    def cost_per_qty_data(self) -> 'model.cost.CostPerQtyData':
        """Compiles and returns teh cost per qty data for the instance."""
        data = {}
        data.update(dict(self.cost_ref_subject_quantity.persistable_data))
        data['cost_per_g'] = self._cost_per_g_
        return data

    @property
    def cost_ref_subject_quantity(self) -> 'model.quantity.HasSettableQuantityOf':
        """Returns the subject quantity instance."""
        # Override to return the local instance, now we have one;
        return self._cost_ref_qty

    def set_cost(self, cost_gbp: Optional[float], qty: Optional[float] = None, unit: str = 'g') -> None:
        """Sets the cost in gbp of any quanitity of any unit."""

        # If either of the values are None, just set to None;
        if qty is None or cost_gbp is None:
            self._cost_per_g_ = None
            return

        # Validate both values;
        cost_gbp = model.cost.validation.validate_cost(cost_gbp)
        qty = model.quantity.validation.validate_nonzero_quantity(qty)

        # Find the ratio of cost per original unit
        r = cost_gbp / qty

        # Convert ratio to grams
        # Find the original quantity in grams;
        g_per_ml = None
        piece_mass_g = None
        if isinstance(self, model.quantity.HasReadableExtendedUnits):
            g_per_ml = self.g_per_ml if self.density_is_defined else None
            piece_mass_g = self.piece_mass_g if self.piece_mass_is_defined else None
        k = model.quantity.convert_qty_unit(
            qty=1,
            start_unit=unit,
            end_unit='g',
            g_per_ml=g_per_ml,
            piece_mass_g=piece_mass_g
        )

        # Calculate the final ratio;
        cost_per_g = r / k

        # Set the value;
        self._cost_per_g_ = cost_per_g
        self.cost_ref_subject_quantity.set_quantity(
            quantity=qty,
            unit=unit
        )

    def load_data(self, data: Dict[str, Any]) -> None:
        """Load data into the instance."""
        # Load the data on the superclass;
        super().load_data(data)

        # If there is no cost data in the dict, just return;
        if 'cost_per_qty_data' not in data.keys():
            return

        # Load the data on this isntance;
        self._cost_ref_qty.load_data(model.quantity.QuantityData(
            quantity_in_g=data['cost_per_qty_data']['quantity_in_g'],
            pref_unit=data['cost_per_qty_data']['pref_unit']
        ))

        self._cost_per_g_ = data['cost_per_qty_data']['cost_per_g']
