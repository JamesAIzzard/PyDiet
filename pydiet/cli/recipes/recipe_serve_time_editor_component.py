from pyconsoleapp import ConsoleAppComponent

from pydiet.cli.shared.exceptions import LetterIntegerParseError

from pydiet.cli.recipes import recipe_edit_service as res
from pydiet.shared import configs as cfg
from pydiet.cli.shared import utility_service as cut

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

    def __init__(self):
        super().__init__()
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
                preset_time=cfg.PRESET_SERVE_TIMES[preset_name]
            )
        # Add these parts into the main template;
        output = _TEMPLATE.format(
            recipe_name=self._res.recipe.name,
            serve_times=serve_times,
            preset_serve_times=preset_serve_times
        )
        output = self.app.fetch_component('standard_page_component').print(output)
        # Return
        return output

    def on_save_changes(self):
        self._res.save_changes()

    def on_include_new_custom_time(self):
        pass

    def dynamic_response(self, raw_response: str) -> None:
        # Try and parse the raw response into a single letter and integer;
        try:
            letter, integer = cut.parse_letter_and_integer(raw_response)
        except LetterIntegerParseError:
            return
        # If we are deleting an existing time;
        if letter == 'd':
            # Try and remove the serve time;
            try:
                self._res.recipe.serve_intervals.pop(integer-1)
            except IndexError:
                return
        # If we are adding a preset time;
        if letter == 'p':
            # Try grab the preset name from the map;
            try:
                p_name = self._res.preset_serve_time_number_map[integer]
            except KeyError:
                return
            # Add the preset time to the recipe;
            self._res.recipe.add_serve_interval(cfg.PRESET_SERVE_TIMES[p_name])
            return