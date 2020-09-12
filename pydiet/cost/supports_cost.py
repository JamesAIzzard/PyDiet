import abc
import copy
from typing import TypedDict, Optional, cast

from pydiet import quantity, cost

class CostData(TypedDict):
    cost_per_g: Optional[float]
    cost_ref_qty: Optional[float]
    cost_ref_units: Optional[str]

def get_empty_cost_data() -> 'CostData':
    return CostData(
        cost_per_g=None,
        cost_ref_qty=None,
        cost_ref_units=None
    )

class SupportsCost(quantity.supports_bulk.SupportsBulk):

    @abc.abstractproperty
    def _cost_data(self) -> 'CostData':
        raise NotImplementedError

    @property
    def readonly_cost_data(self) -> 'CostData':
        return copy.deepcopy(self._cost_data)

    @property
    def cost_per_g(self) -> float:
        if not self.cost_data_fully_defined:
            raise cost.exceptions.CostDataUndefinedError
        return cast(float, self.readonly_cost_data['cost_per_g'])

    @property
    def cost_ref_qty(self) -> float:
        if not self.cost_ref_qty_defined:
            raise cost.exceptions.CostDataUndefinedError
        return cast(float, self.readonly_cost_data['cost_ref_qty'])

    @property
    def cost_ref_units(self) -> str:
        if not self.cost_ref_units_defined:
            raise cost.exceptions.CostDataUndefinedError
        return cast(str, self.readonly_cost_data['cost_ref_units'])

    @property
    def cost_summary(self) -> str:
        if self.cost_data_fully_defined:
            return '£{cost_per_pref_unit:.2f} per {pref_unit}, (£{cost_per_g:.2f} per g)'.format(
                cost_per_pref_unit=self.cost_per_pref_unit,
                pref_unit=self.pref_bulk_units,
                cost_per_g=self.cost_per_g)
        else:
            return 'Undefined'

    @property
    def cost_per_pref_unit(self) -> float:
        '''Returns the cost in GBP per preferred unit. So if the pref unit
        is ml, the £/ml value is returned. If the pref unit is kg,
        the £/kg value is returned.

        Raises:
            cost.exceptions.CostDataUndefinedError: If the rqd data is not set yet.

        Returns:
            float: Cost in GBP per the preferred unit, e.g 1.50 to indicate £1.50/kg
                if the preferred unit is kg.
        '''
        return self.cost_per_g*self.grams_to_pref_units_ratio

    @property
    def cost_data_fully_defined(self) -> bool:
        if None in self.readonly_cost_data.values():
            return False
        else:
            return True

    @property
    def cost_per_g_defined(self) -> bool:
        if self.readonly_cost_data['cost_per_g'] == None:
            return False
        else:
            return True

    @property
    def cost_ref_qty_defined(self) -> bool:
        if self.readonly_cost_data['cost_ref_qty'] == None:
            return False
        else:
            return True

    @property
    def cost_ref_units_defined(self) -> bool:
        if self.readonly_cost_data['cost_ref_units'] == None:
            return False
        else:
            return True  




class SupportsCostSetting(SupportsCost):

    def set_cost_per_g(self, cost_per_g: float) -> None:
        cost_per_g = cost.cost_service.validate_cost(cost_per_g)
        self._cost_data['cost_per_g'] = cost_per_g

    def set_cost_ref_qty(self, cost_ref_qty: float) -> None:
        if cost_ref_qty < 0:
            raise ValueError('Cost reference quantity must be a positive number.')
        self._cost_data['cost_ref_qty'] = cost_ref_qty

    def set_cost_ref_units(self, cost_ref_units:str) -> None:
        # Check unit is legit;
        cost_ref_units = quantity.quantity_service.validate_qty_unit(cost_ref_units)

        # Prevent piece or volumes being used where not defined;
        if cost_ref_units in quantity.quantity_service.get_recognised_vol_units():
            if not self.density_is_defined:
                raise quantity.exceptions.DensityDataUndefinedError
        elif cost_ref_units == quantity.supports_bulk.BulkTypes.PIECE:
            if not self.piece_mass_defined:
                raise quantity.exceptions.PcMassDataUndefinedError

        # Assign
        self._cost_data['cost_ref_units'] = cost_ref_units
