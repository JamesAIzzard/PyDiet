from pyconsoleapp.parse_tools import parse_letter_and_integer
from textwrap import fill

from pyconsoleapp import ConsoleAppComponent, parse_tools
from pyconsoleapp import configs as console_configs

from pydiet.recipes import recipe_edit_service as res

_TEMPLATE = '''Recipe Step Editor:

{steps}

(s)  -- Save Changes

(a)  -- Add new step
(e*) -- Edit step
(r*) -- Remove step
(u*) -- Move step * up list
(d*) -- Move step * down list
'''

_STEP_TEMPLATE = '{number}. {step_text}\n\n'

class RecipeStepEditMenuComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app)
        self._res = res.RecipeEditService()
        self.set_option_response('s', self.on_save_changes)
        self.set_option_response('a', self.on_add_step)

    def print(self):
        # Build the step summary;
        steps = ''
        if len(self._res.recipe.steps):
            for step_num in self._res.recipe.steps.keys():
                steps = steps + _STEP_TEMPLATE.format(
                    number=step_num,
                    step_text = fill(self._res.recipe.steps[step_num], 
                        console_configs.terminal_width_chars)
                )
        else:
            steps = 'No steps added yet.'
        # Assemble main template;
        output = _TEMPLATE.format(steps=steps)
        return self.app.fetch_component('standard_page_component').call_print(output)

    def on_save_changes(self):
        self._res.save_changes()

    def on_add_step(self):
        # Redirect to the step editor
        self.app.goto('home.recipes.edit.steps.edit_step')

    def dynamic_response(self, raw_response: str) -> None:
        # Try and parse the raw response into letter and integer;
        try:
            letter, step_number = parse_tools.parse_letter_and_integer(raw_response)
        except parse_tools.LetterIntegerParseError:
            return
        # Check the integer references a step on the list;
        if step_number > len(self._res.recipe.steps) or step_number < 1:
            return
        # If we are editing a step;
        if letter == 'e':
            # Select the step;
            self._res.selected_step_number = step_number
            # Redirect to editor;
            self.app.goto('home.recipes.edit.steps.edit_step')
        # If we are removing a step;
        if letter == 'r':
            self._res.recipe.remove_step(step_number)
        # If we are moving a step upwards;
        if letter == 'u':
            if step_number > 1:
                self._res.recipe.move_step(step_number, step_number-1)
        # If we are moving a step downwards;
        if letter == 'd':
            if step_number < len(self._res.recipe.steps):
                self._res.recipe.move_step(step_number, step_number+1)
