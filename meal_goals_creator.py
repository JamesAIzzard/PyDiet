import goals
import persistence

data = goals.MealGoalsData(
    flags={
        "alcohol_free": True,
        "vegetarian": True
    },
    max_cost_gbp_target=5.00,
    calorie_target=600,
    nutrient_mass_goals={
        "protein": {
            "nutrient_mass_g": 30,
            "nutrient_pref_units": 'g'
        },
        "carbohydrate": {
            "nutrient_mass_g": 35,
            "nutrient_pref_units": 'g'
        }
    },
    name="Test Breakfast",
    time="07:00",
    tags=["main", "drink"]
)

mg = goals.PersistableMealGoals(meal_goals_data=data)
persistence.save(mg)
