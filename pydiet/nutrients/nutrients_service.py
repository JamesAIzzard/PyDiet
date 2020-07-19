from pydiet import nutrients


def print_nutrient_targets_menu(subject: 'nutrients.i_has_nutrient_targets.IHasNutrientTargets') -> str:
    output = ''
    if len(subject.nutrient_targets):
        for i, nutrient_name in enumerate(subject.nutrient_targets.keys(), start=1):
            output = output + '{num}. {nutrient_name} - {nutrient_qty}{nutrient_qty_units}'.format(
                num=i,
                nutrient_name=nutrient_name,
                nutrient_qty=subject.nutrient_targets[nutrient_name][0],
                nutrient_qty_units=subject.nutrient_targets[nutrient_name][1])
    else:
        output = 'No nutrient targets assigned.'
    return output
