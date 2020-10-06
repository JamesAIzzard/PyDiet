from typing import Dict

from pyconsoleapp import ConsoleAppComponent
from pyconsoleapp import menu_tools, parse_tools

from pydiet.recipes import recipe_edit_service as res
from pydiet import configs

_TEMPLATE = '''Recipe Tags:
------------------------
{current_tags}
(s) -- Save Changes
(d*) -- Delete (where * = number)

Add Tags:
{addable_tags}

'''

class RecipeTagEditorComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self._res = res.RecipeEditService()
        self.set_option_response('s', self.on_save_changes)

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
            current_tags = 'No tags assigned.\n'
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
        output = self.app.fetch_component('standard_page_component').call_print(output)
        return output

    def on_save_changes(self):
        self._res.save_changes()

    def dynamic_response(self, raw_response: str) -> None:
        # Cache tag maps;
        atm = self.addable_tag_map
        ctm = self.current_tag_map
        # Try and parse the raw response into a single letter and integer;
        try:
            letter, integer = parse_tools.parse_letter_and_integer(raw_response)
        except parse_tools.LetterIntegerParseError:
            return
        # If we are adding a tag;
        if letter == 'a':
            # If the integer refers to an item on the addable tag list;
            if integer <= len(atm):
                # Add the referenced tag to the recipe;
                self._res.recipe.add_tag(atm[integer])
        # If we are deleting a tag;
        elif letter == 'd':
            # If the integer refers to an item on the current tag list;
            if integer <= len(ctm):
                # Delete the referenced tag from the recipe;
                self._res.recipe.remove_tag(ctm[integer])

        
