from pydiet.nutrients import (
    nutrients_service,
    i_nutrient_targetable)

def print_nutrient_targets_menu(subject:'i_nutrient_targetable.INutrientTargetable')->str:
    output = ''
    if len(subject.nutrient_targets):
        for i,nutrient_name in enumerate(subject.nutrient_targets.keys(), start=1):
            output = output + '{num}. {nutrient_name} - {nutrient_qty}{nutrient_qty_units}'.format(
                num=i,
                nutrient_name=nutrient_name,
                nutrient_qty=subject.nutrient_targets[nutrient_name][0],
                nutrient_qty_units=subject.nutrient_targets[nutrient_name][1])
    else:
        output = 'No nutrient targets assigned.'
    return output