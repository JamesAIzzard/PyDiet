from typing import TYPE_CHECKING

from pydiet import cost, quantity

if TYPE_CHECKING:
    from pydiet.cost.supports_cost import SupportsCost

def print_general_cost_summary(subject: 'cost.supports_general_cost.SupportsGeneralCost') -> str:
    if not subject.cost_is_defined:
        return 'Undefined'
    else:
        qts = quantity.quantity_service  # For easy typing.
        if subject.pref_cost_qty_units in qts.get_recognised_mass_units():
            qty = qts.convert_mass_units(1, 'g', subject.pref_cost_qty_units)
        elif subject.pref_cost_qty_units in qts.get_recognised_vol_units():
            qty = qts.convert_mass_to_volume
        return '£{cost:.2f}/{qty}{qty_units}'.format(
            cost=subject.readonly_cost_data['cost'],
            qty=subject.readonly_cost_data['mass_g'],
            qty_units=subject.readonly_cost_data['pref_qty_units']
        )
