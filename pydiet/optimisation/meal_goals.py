_data_template = {
    "time": None,
    "max_cost_gbp": None,
    "flags": [],    
    "components": [],
    "perc_total_cals": None,
    "total_perc_fat": None,
    "total_perc_carbs": None,
    "total_perc_protein": None,    
    "nutrient_mass_targets": {}    
}

class MealGoals():
    def __init__(self, data):
        self._data = data
        self._applied_recipes = {}