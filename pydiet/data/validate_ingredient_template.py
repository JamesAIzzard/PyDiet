# Add root module to path;
import sys, os
# sys.path.append('/home/james/Documents/PyDiet')
sys.path.append('c:\\Users\\james.izzard\\Documents\\PyDiet')

from pydiet.data import repository_service as rs
import pydiet.configs as configs

# Bring the template in;
template = rs.read_ingredient_data_template()

# Check that all the nutrient alias keys match against
# names in the template;
for alias_key in configs.NUTRIENT_ALIASES.keys():
    if not alias_key in template['groups'].keys() and \
    not alias_key in template['molecules'].keys():
        raise ValueError('The alias key {} was not found in the template.'.format(alias_key))

# Check that none of the alias's are keys in the template;
for alias_key in configs.NUTRIENT_ALIASES.keys():
    for alias in configs.NUTRIENT_ALIASES[alias_key]:
        if alias in template['groups'].keys() or \
            alias in template['molecules'].keys():
            raise ValueError('The alias {} is also a key in the template.'.format(alias))

# Check that none of the nutrient group names also
# appear in the template as molecules;
for group_name in configs.NUTRIENT_GROUP_DEFINITIONS.keys():
    if group_name in template['molecules'].keys():
        raise ValueError('The group name {} also appears in the template as a molecule.'.format(group_name))

# Check that all of the molecules listed under the
# groups appear in the template as molecules or groups;
for group_name in configs.NUTRIENT_GROUP_DEFINITIONS.keys():
    for molecule in configs.NUTRIENT_GROUP_DEFINITIONS[group_name]:
        if not molecule in template['molecules'].keys() and not molecule in template['groups'].keys():
            raise ValueError('The molecule {} is listed in the group {} but is not listed in the template.'.format(molecule, group_name))

# Check that all groups listed on the group defintions
# appear as groups in the template, and vice-versa;
for group_name in configs.NUTRIENT_GROUP_DEFINITIONS.keys():
    if not group_name in template['groups'].keys():
        raise ValueError('The group {} is listed in the group definitions, but not on the template.'.format(group_name))
for group_name in template['groups'].keys():
    if not group_name in configs.NUTRIENT_GROUP_DEFINITIONS.keys():
        raise ValueError('The group {} is listed on the template, but not in the group definitions.'.format(group_name))

# Rewrite the template to sort alphabetically;
rs.update_ingredient_data(
    template, configs.INGREDIENT_DATAFILE_TEMPLATE_NAME
)