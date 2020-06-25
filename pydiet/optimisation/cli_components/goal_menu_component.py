from typing import Dict

from pyconsoleapp import ConsoleAppComponent, menu_tools, parse_tools

from pydiet.optimisation import optimisation_service as ops
from pydiet.optimisation import optimisation_edit_service as oes
from pydiet import repository_service as rps

_MAIN = '''Day Goals:

1. Training Day
2. Recovery Day
3. Rest Day
{day_goals}

(a)  -- Add a new day.
(e*) -- Edit a day.
(d*) -- Delete a day.
(m)  -- Manage global goals.
(s)  -- Save changes.

'''


class GoalMenuComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self._oes = oes.OptimisationEditService()
        self.day_goals_menu = ''
        self.num_day_goals:int = 0
        self.numbered_day_goals:Dict[int, str] = {}
        self.set_option_response('a', self.on_add_new_day)
        self.set_option_response('m', self.on_manage_global_goals)
        self.set_option_response('s', self.on_save_changes)

    def run(self) -> None:
        # Build the day goals menu;
        # Read the day_goals index;
        dg_index = rps.read_day_goals_index()
        # Stash the number of saved day goals;
        self.num_day_goals = len(dg_index)
        # Get a dictionary of names & numbers
        # (save for dynamic response later);
        self.numbered_day_goals = menu_tools.create_number_name_map(
            list(dg_index.values()))
        # Cycle though the dict and build the menu;
        output = ''
        for dg_num in self.numbered_day_goals.keys():
            output = output + "{dg_num}. {dg_name}\n".format(
                dg_num=dg_num,
                dg_name=self.numbered_day_goals[dg_num]
            )
        self.day_goals_menu = output

    def print(self, *args, **kwargs) -> str:
        # Create the content;
        output = _MAIN.format(day_goals=self.day_goals_menu)
        # Format and return the template;
        output = self.app.fetch_component(
            'standard_page_component').print(output)
        return output

    def on_add_new_day(self) -> None:
        # Put a new DayGoals into scope;
        self._oes.day_goals = ops.load_new_day_goals()
        # Configure the save output reminder;
        self.app.guard_exit('home.day_goals.edit', 'DayGoalsSaveCheckComponent')
        # Navigate to editor;
        self.app.goto('home.day_goals.edit')

    def on_manage_global_goals(self)->None:
        raise NotImplementedError

    def on_save_changes(self)->None:
        raise NotImplementedError

    def dynamic_response(self, raw_response: str) -> None:
        # Try and parse the response into a letter and integer;
        try:
            letter, day_num = parse_tools.parse_letter_and_integer(raw_response)
        except parse_tools.LetterIntegerParseError:
            return
        # Check the day number does actually refer to a day_goals instance;
        if day_num <= 0 or day_num > self.num_day_goals:
            return
        # If we are editing a day;
        if letter == 'e':
            # Get the day_goals name;
            dg_datafile_name = ops.convert_day_goals_name_to_datafile_name(
                self.numbered_day_goals[day_num])
            # Load the day into the edit service;
            self._oes.day_goals = ops.load_day_goals(dg_datafile_name)
            # Redirect to day goals editor;
            self.app.goto('DayGoalsEditorComponent')
        # If we are deleting a day;
        elif letter == 'd':
            pass
        
