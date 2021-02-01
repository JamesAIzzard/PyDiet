from model import FlagNutrientRelations
from model.flag_nutrient_relation import ImpliesNutrientIs as Implies

flag_nutrient_relations = FlagNutrientRelations([
    {"flag_name": "alcohol-free", "nutrient_name": "alcohol", "implies_nutrient_is": Implies.ZERO},
    {"flag_name": "lactose-free", "nutrient_name": "lactose", "implies_nutrient_is": Implies.ZERO}
])
