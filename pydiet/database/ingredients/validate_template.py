# Add root module to path;
import sys, os
sys.path.append('/home/james/Documents/PyDiet')

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

# TODO - Check that none of the nutrient group names also
# appear in the template as molecules;

# TODO - Check that all of the molecules listed under the
# groups appear in the template as molecules;

# Rewrite the template to sort alphabetically;
rs.update_ingredient_data(
    template, configs.INGREDIENT_DATAFILE_TEMPLATE_NAME
)

pass