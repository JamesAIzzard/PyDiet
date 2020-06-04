from typing import Dict

from pyconsoleapp import ConsoleAppComponent
from pyconsoleapp import menu_tools

from pydiet.recipes import recipe_edit_service as res
from pydiet import configs

_TEMPLATE = '''Recipe Tags:
------------------------
{current_tags}
(s) -- Save Changes
(d*) -- Delete (where * = number)

Add Tags:
{addable_tags}
(You can add or delete multiple tags 
seperated with a comma, 
e.g. "a1, a2" or "d1, d2")

'''

class RecipeTagEditorComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self._res = res.RecipeEditService()

    @property
    def current_tag_map(self) -> Dict[int, str]:
        return menu_tools.create_number_name_map(
            self._res.recipe.tags)

    @property
    def addable_tag_map(self) -> Dict[int, str]:
        # First build a list of all tags minus
        # those already added;
        addable_tags = configs.RECIPE_TAGS.copy()
        for tag in self._res.recipe.tags:
            if tag in addable_tags:
                addable_tags.remove(tag)
        # Turn it into numbered map;
        return menu_tools.create_number_name_map(addable_tags)

    def run(self):
        # If there is no recipe loaded;
        if not self._res.recipe:
            # Go back to the main recipe state;
            self.goto('home.recipes')

    def print(self):
        # First build the current tag list;
        current_tags = ''
        ## If there are tags assigned;
        if len(self._res.recipe.tags):
            # Grab a numbered list;
            tm = self.current_tag_map
            for key in tm.keys():
                current_tags = current_tags + '{} -- {}\n'.format(
                    key, tm[key])
        ## If there are no tags assigned;
        elif len(self._res.recipe.tags) == 0:
            current_tags = 'No tags assigned.'
        # Build the available tag list;
        addable_tags = ''
        atm = self.addable_tag_map
        for key in atm.keys():
            addable_tags = addable_tags + '(a{}) -- {}\n'.format(
                key, atm[key])
        # Return the main template;
        output = _TEMPLATE.format(
            current_tags=current_tags,
            addable_tags=addable_tags
        )
        output = self.app.fetch_component('standard_page_component').print(output)
        return output
