from pydiet.shared.configs import PRESET_SERVE_TIMES
from typing import TYPE_CHECKING

from pinjector import inject
from pyconsoleapp import ConsoleAppComponent

if TYPE_CHECKING:
    from pydiet.cli.recipes.recipe_edit_service import RecipeEditService
    from pydiet.shared import configs

_TEMPLATE = '''Recipe Serve Times:
-------------------

{recipe_name} can be served at the following times:
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
        self._res:'RecipeEditService' = inject('pydiet.cli.recipe_edit_service')
        self._cf:'configs' = inject('pydiet.configs')
        self.set_option_response('s', self.on_save_changes)
        self.set_option_response('n', self.on_include_new_custom_time)

    def print(self):
        # Build the serve times display;
        serve_times = ''
        for time_num in self._res.serve_time_number_map:
            serve_times = serve_times + '{num}. {time}\n'.format(
                num=time_num,
                time=self._res.serve_time_number_map[time_num]
            )     
        # Build the preset serve times display;
        preset_serve_times = ''
        for time_num in self._res.preset_serve_time_number_map:
            preset_name = self._res.preset_serve_time_number_map[time_num]
            preset_serve_times = preset_serve_times + '(p{num}) -- {preset_name}: {preset_time}\n'.format(
                num=time_num,
                preset_name=preset_name,
                preset_time=self._cf.PRESET_SERVE_TIMES[preset_name]
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
        pass