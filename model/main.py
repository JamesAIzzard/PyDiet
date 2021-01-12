import model
from model import nutrients

# Init the model;
nutrients.validation.validate_configs()
model.build_flag_nutrient_rel_maps()
nutrients.build_global_nutrients()