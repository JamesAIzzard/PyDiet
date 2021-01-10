from pyconsoleapp import ConsoleAppComponent, parse_tools

from pydiet.recipes import recipe_edit_service as res
from pydiet import configs

_TEMPLATE = '''{recipe_name} can be served at the following times:
-------------------
{serve_times}
(e*) -- Edit | (d*) -- Delete (where * = number)

------------------------------------------

(s) -- Save Changes

Add Preset Times:
{preset_serve_times}

(n) -- Include New Custom Time

'''

class RecipeServeTimeEditorComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app)
        self._res = res.RecipeEditService()
        self.set_option_response('s', self.on_save_changes)
        self.set_option_response('n', self.on_include_new_custom_time)

    def print(self):
        # Build the serve times display;
        serve_times = ''
        if len(self._res.recipe.serve_intervals):
            for time_num in self._res.serve_time_number_map:
                serve_times = serve_times + '{num}. {time}\n'.format(
                    num=time_num,
                    time=self._res.serve_time_number_map[time_num]
                )
        else:
            serve_times = 'No serve times added yet.\n'     
        # Build the preset serve times display;
        preset_serve_times = ''
        for time_num in self._res.preset_serve_time_number_map:
            preset_name = self._res.preset_serve_time_number_map[time_num]
            preset_serve_times = preset_serve_times + '(p{num}) -- {preset_name}: {preset_time}\n'.format(
                num=time_num,
                preset_name=preset_name,
                preset_time=configs.PRESET_SERVE_TIMES[preset_name]
            )
        # Add these parts into the main template;
        output = _TEMPLATE.format(
            recipe_name=self._res.recipe.name,
            serve_times=serve_times,
            preset_serve_times=preset_serve_times
        )
        output = self.app.fetch_component('standard_page_component').call_print(output)
        # Return
        return output

    def on_save_changes(self):
        self._res.save_changes()

    def on_include_new_custom_time(self):
        # Make sure there is no selected index (to prevent editing existing one);
        self._res.selected_serve_time_index = None
        # Redirect to interval editor;
        self.app.goto('.edit_interval')

    def dynamic_response(self, raw_response: str) -> None:
        # Try and parse the raw response into a single letter and integer;
        try:
            letter, integer = parse_tools.parse_letter_and_integer(raw_response)
        except parse_tools.LetterIntegerParseError:
            return
        # If we are adding a preset time;
        if letter == 'p':
            # Try grab the preset name from the map;
            try:
                p_name = self._res.preset_serve_time_number_map[integer]
            except KeyError:
                return
            # Add the preset time to the recipe;
            self._res.recipe.add_serve_interval(configs.PRESET_SERVE_TIMES[p_name])
            return            
        # Check the integer references an interval on the list;
        if integer > len(self._res.recipe.serve_intervals) or integer < 1:
            return
        # If we are deleting an existing time;
        elif letter == 'd':
            # Remove the serve time;
            self._res.recipe.serve_intervals.pop(integer-1)
            return
        # If we are editing an existing time;
        elif letter == 'e':
            # Select the serve time;
            self._res.selected_serve_time_index = integer-1
            # Redirect to editor;
            self.app.goto('.edit_interval')
            return

