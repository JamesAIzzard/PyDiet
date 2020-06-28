from typing import Dict

from pyconsoleapp import ConsoleAppComponent, menu_tools, parse_tools

from pydiet.optimisation import optimisation_service as ops
from pydiet.optimisation import optimisation_edit_service as oes
from pydiet import repository_service as rps
from pydiet.optimisation.exceptions import DuplicateDayGoalsNameError

_MAIN = '''Day Goals:

{day_goals}

(-a [day name])   -> Add a new day.
(-e [day number]) -> Edit a day.
(-d [day number]) -> Delete a day.
(-m)              -> Manage global goals.
(-s)              -> Save changes.

'''


class GoalMenuComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self._oes = oes.OptimisationEditService()
        self.day_goals_menu = ''
        self.num_day_goals:int = 0
        self.numbered_day_goals:Dict[int, str] = {}
        self.set_option_response('-m', self.on_manage_global_goals)
        self.set_option_response('-s', self.on_save_changes)

    def run(self) -> None:
        # Build the day goals menu;
        # First, read the day_goals index;
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

    def on_manage_global_goals(self)->None:
        raise NotImplementedError

    def on_save_changes(self)->None:
        raise NotImplementedError

    def dynamic_response(self, raw_response: str) -> None:
        # Parse response into flags and text;
        flags, text = parse_tools.parse_flags_and_text(raw_response)

        # If we are adding a new day;
        if flags == ['-a']:
            # Check that the name has been provided;
            if not text:
                self.app.error_message = 'The day name must be provided.'
                return
            # Create a new DayGoals instance;
            dg = ops.load_new_day_goals()
            try:
                dg.name = text
            except DuplicateDayGoalsNameError:
                self.app.error_message = 'There is already a day called {day_goals_name}'.format(day_goals_name=text)
            # Place it on the scope;
            self._oes.day_goals = dg
            # Configure the save output reminder;
            self.app.guard_exit('home.goals.edit_day', 'DayGoalsSaveCheckComponent')
            # Navigate to editor;
            self.app.goto('home.goals.edit_day')
            return

        # If we are editing a day;
        elif flags == ['-e']:
            # Check the text is a corresponds to a dg number;
            if not text:
                self.app.info_message = 'A selection number must be specified.'
                return
            try:
                day_num = int(text)
            except ValueError:
                return
            if day_num < 1 or day_num > self.num_day_goals:
                return
            # Get the day_goals name;
            dg_datafile_name = ops.convert_day_goals_name_to_datafile_name(
                self.numbered_day_goals[day_num])
            # Load the day into the edit service;
            self._oes.day_goals = ops.load_day_goals(dg_datafile_name)
            # Redirect to day goals editor;
            self.app.goto('home.goals.edit_day')

        # If we are deleting a day;
        elif flags == ['-d']:
            pass
        
