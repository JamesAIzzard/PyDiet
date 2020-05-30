import json
import sys

from pydiet.data import repository_service as rps
from pydiet.shared import configs as cfg

# If running this module in isolation;
if __name__ == '__main__':
    ## sys.path.append('/home/james/Documents/PyDiet')
    sys.path.append('c:\\Users\\james.izzard\\Documents\\PyDiet')
    ## sys.path.append('c:\\Users\\James Izzard\\Documents\\PyDiet')


# Bring the template in;
template = rps.read_ingredient_template_data()

# Check that all the nutrient alias keys match against
# names in the template;
for alias_key in cfg.NUTRIENT_ALIASES.keys():
    if not alias_key in template['nutrients'].keys():
        raise ValueError('The alias key {} was not listed as a nutrient in the template.'.format(alias_key))

# Check that none of the alias's are also nutrient names in the template;
for alias_key in cfg.NUTRIENT_ALIASES.keys():
    for alias in cfg.NUTRIENT_ALIASES[alias_key]:
        if alias in template['nutrients'].keys():
            raise ValueError('The alias {} is also a nutrient name in the template.'.format(alias))

# Check that all of the nutrients listed under the
# groups appear in the template as nutrients;
for group_name in cfg.NUTRIENT_GROUP_DEFINITIONS.keys():
    for nutrient in cfg.NUTRIENT_GROUP_DEFINITIONS[group_name]:
        if not nutrient in template['nutrients'].keys():
            raise ValueError('The nutrient {} is listed in the group {} but is not listed in the template.'.format(nutrient, group_name))

# Check that all groups listed on the group defintions
# appear as nutrients in the template, and vice-versa;
for group_name in cfg.NUTRIENT_GROUP_DEFINITIONS.keys():
    if not group_name in template['nutrients'].keys():
        raise ValueError('The nutrient {} is listed in the group definitions, but not on the template.'.format(group_name))

# Check that the all nutrient-flag rels relate to nutrients
# and flags which exist in the template;
for flag_name in cfg.NUTRIENT_FLAG_RELS.keys():
    ## Check the flag exists;
    if not flag_name in template['flags'].keys():
        raise ValueError('{} is not listed as a flag in the template.'.format(flag_name))
    ## Check each of the nutrients referenced exists;
    for nutrient_name in cfg.NUTRIENT_FLAG_RELS[flag_name]:
        if not nutrient_name in template['nutrients'].keys():
            raise ValueError('{nutrient_name} is associated with the flag {flag_name}, but does not appear as a nutrient in the template.'.format(
            nutrient_name=nutrient_name,
            flag_name=flag_name
        ))

# Rewrite the template to sort alphabetically;
with open(cfg.INGREDIENT_DB_PATH+'{}.json'.
            format(cfg.INGREDIENT_DATAFILE_TEMPLATE_NAME), 'r+') as fh:
    json.dump(template, fh, indent=2, sort_keys=True)

if __name__ == '__main__':
    print('Ingredient templated passed validation.')