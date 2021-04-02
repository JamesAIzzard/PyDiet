def set_18_g_protein_goal(obj: 'goals.HasSettableGoals') -> 'goals.HasSettableGoals':
    obj.set_nutrient_mass_goal(
        nutrient_name="protein",
        nutrient_mass=18,
        nutrient_mass_unit='g'
    )
    return obj
