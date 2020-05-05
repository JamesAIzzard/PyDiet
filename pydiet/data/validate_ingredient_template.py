import json

# Add root module to path;
import sys, os
# sys.path.append('/home/james/Documents/PyDiet')
sys.path.append('c:\\Users\\james.izzard\\Documents\\PyDiet')
# sys.path.append('c:\\Users\\James Izzard\\Documents\\PyDiet')

from pydiet.data import repository_service as rs
import pydiet.shared.configs as configs

# Bring the template in;
template = rs.read_ingredient_template_data()

# Check that all the nutrient alias keys match against
# names in the template;
for alias_key in configs.NUTRIENT_ALIASES.keys():
    if not alias_key in template['nutrients'].keys():
        raise ValueError('The alias key {} was not listed as a nutrient in the template.'.format(alias_key))

# Check that none of the alias's are also nutrient names in the template;
for alias_key in configs.NUTRIENT_ALIASES.keys():
    for alias in configs.NUTRIENT_ALIASES[alias_key]:
        if alias in template['nutrients'].keys():
            raise ValueError('The alias {} is also a nutrient name in the template.'.format(alias))

# Check that all of the nutrients listed under the
# groups appear in the template as nutrients;
for group_name in configs.NUTRIENT_GROUP_DEFINITIONS.keys():
    for nutrient in configs.NUTRIENT_GROUP_DEFINITIONS[group_name]:
        if not nutrient in template['nutrients'].keys():
            raise ValueError('The nutrient {} is listed in the group {} but is not listed in the template.'.format(nutrient, group_name))

# Check that all groups listed on the group defintions
# appear as nutrients in the template, and vice-versa;
for group_name in configs.NUTRIENT_GROUP_DEFINITIONS.keys():
    if not group_name in template['nutrients'].keys():
        raise ValueError('The nutrient {} is listed in the group definitions, but not on the template.'.format(group_name))

# Rewrite the template to sort alphabetically;
with open(configs.INGREDIENT_DB_PATH+'{}.json'.
            format(configs.INGREDIENT_DATAFILE_TEMPLATE_NAME), 'r+') as fh:
    json.dump(template, fh, indent=2, sort_keys=True)