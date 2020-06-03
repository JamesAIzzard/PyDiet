from pyconsoleapp import ConsoleAppComponent

from pydiet.recipes import recipe_service as rps
from pydiet.recipes import recipe_edit_service

_TEMPLATE = '''
Enter a time interval in 24hr format:
hh:mm-hh:mm{current_value}
-------------------------------------
'''
_CURRENT_VALUE_TEMPLATE = '\n(Current Value: {})'


class TimeIntervalEditorComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app)
        self._res = recipe_edit_service.RecipeEditService()

    def print(self):
        # If we are editing, build the current value;
        current_value = ''
        if not self._res.selected_serve_time_index == None:
            current_value = _CURRENT_VALUE_TEMPLATE.format(
                self._res.recipe.serve_intervals[
                    self._res.selected_serve_time_index])
        output = _TEMPLATE.format(current_value=current_value)
        output = self.app.fetch_component(
            'standard_page_component').print(output)
        return output

    def dynamic_response(self, raw_response: str) -> None:
        # First, validate the interval;
        try:
            serve_interval = rps.parse_time_interval(raw_response)
        except (rps.TimeIntervalParseError, rps.TimeIntervalValueError):
            self.app.error_message = 'Unable to parse {} into a time interval.'.format(
                raw_response)
            return
        # If the index is set, update and clear index;
        if not self._res.selected_serve_time_index == None:
            self._res.recipe.update_serve_interval(
                serve_interval,
                self._res.selected_serve_time_index
            )
            self._res.selected_serve_time_index = None
            self.app.info_message = 'Serve interval updated.'
        # Otherwise, add;
        else:
            self._res.recipe.add_serve_interval(serve_interval)
            self.app.info_message = 'Serve interval added.'
        # Go back to serve times menu;
        self.app.goto('home.recipes.edit.serve_times')
