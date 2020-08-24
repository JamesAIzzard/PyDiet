from pydiet import cost


def print_cost_summary(subject: 'cost.i_has_cost.IHasCost') -> str:
    if not subject.cost_is_defined:
        return 'Undefined'
    else:
        return '£{cost:.2f}/{qty}{qty_units}'.format(
            cost=subject.cost_data['cost'],
            qty=subject.cost_data['qty'],
            qty_units=subject.cost_data['qty_units']
        )
