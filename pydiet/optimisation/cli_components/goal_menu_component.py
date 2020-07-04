from typing import Dict, Optional

from pyconsoleapp import ConsoleAppComponent, menu_tools, parse_tools

from pydiet.optimisation import optimisation_service as ops
from pydiet.optimisation import optimisation_edit_service as oes
from pydiet import repository_service as rps
from pydiet.optimisation.exceptions import DuplicateDayGoalsNameError

_MAIN = '''Day Goals:

{day_goals}
-add, -a       [day name]     -> Add a new day.
-edit, -e      [day number]   -> Edit a day.
-delete, -d    [day number]   -> Delete a day.
-globals, -g                  -> Manage global daily nutrient targets.
-save, -s                     -> Save changes.

'''


class GoalMenuComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self._oes = oes.OptimisationEditService()
        self.day_goals_menu = ''
        self.num_day_goals: int = 0
        self.numbered_day_goals: Dict[int, str] = {}
        self.set_response_function(['-a', '-add'], self.on_add_day)
        self.set_response_function(['-e', '-edit'], self.on_edit_day)
        self.set_response_function(['-d', '-delete'], self.on_delete_day)
        self.set_response_function(['-g', '-globals'], self.on_manage_global_goals)
        self.set_response_function(['-s', '-save'], self.on_save_changes)

    def _parse_day_goals_num(self, text: Optional[str]) -> int:
        if not text:
            raise ValueError
        day_num = int(text)
        if day_num < 1 or day_num > self.num_day_goals:
            raise ValueError
        return day_num

    def run(self) -> None:
        # First, read the day_goals index;
        dg_index = rps.read_day_goals_index()
        # Stash the number of saved day goals;
        self.num_day_goals = len(dg_index)
        # Get a dictionary of names & numbers
        # (save for dynamic response later);
        self.numbered_day_goals = menu_tools.create_number_name_map(
            list(dg_index.values()))

        # Build the menu;
        output = ''
        if self.num_day_goals > 0:
            for dg_num in self.numbered_day_goals.keys():
                output = output + "{dg_num}. {dg_name}\n".format(
                    dg_num=dg_num,
                    dg_name=self.numbered_day_goals[dg_num]
                )
        else:
            output = 'No day goals to show.\n'
        self.day_goals_menu = output

    def print(self, *args, **kwargs) -> str:
        # Create the content;
        output = _MAIN.format(day_goals=self.day_goals_menu)
        # Format and return the template;
        output = self.app.fetch_component(
            'standard_page_component').print(output)
        return output

    def on_manage_global_goals(self) -> None:
        # Set a guard to check for save on exit;
        # Navigate to the global goals editor;
        self.app.goto('home.goals.edit_globals')

    def on_add_day(self, text=None) -> None:
        # Check the day name arg was provided;
        if not text:
            self.app.error_message = 'The day name must be provided.'
            return

        # Create a new DayGoals instance;
        dg = ops.load_new_day_goals()
        try:
            dg.name = text
        except DuplicateDayGoalsNameError:
            self.app.error_message = 'There is already a day called {day_goals_name}'.format(
                day_goals_name=text)

        # Place it on the scope;
        self._oes.day_goals = dg

        # Configure the save output reminder;
        self.app.guard_exit('home.goals.edit_day',
                            'DayGoalsSaveCheckComponent')

        # Navigate to editor;
        self.app.goto('home.goals.edit_day')
        return

    def on_edit_day(self, text=None) -> None:
        try:
            day_num = self._parse_day_goals_num(text)
        except ValueError:
            return
        # Get the day_goals name;
        dg_datafile_name = ops.convert_day_goals_name_to_datafile_name(
            self.numbered_day_goals[day_num])
        # Load the day into the edit service;
        self._oes.day_goals = ops.load_day_goals(dg_datafile_name)
        # Don't forget the datafile name!;
        self._oes.datafile_name = dg_datafile_name
        # Configure the save output reminder;
        self.app.guard_exit('home.goals.edit_day',
                            'DayGoalsSaveCheckComponent')
        # Redirect to day goals editor;
        self.app.goto('home.goals.edit_day')

    def on_delete_day(self, text=None) -> None:
        try:
            day_num = self._parse_day_goals_num(text)
        except ValueError:
            return
        # Get the datafile name;
        df_to_delete = ops.convert_day_goals_name_to_datafile_name(
            self.numbered_day_goals[day_num])
        # Put details on the edit service;
        self._oes.datafile_name = df_to_delete
        self._oes.day_goals = ops.load_day_goals(df_to_delete)
        # Navigate to confirm;
        self.app.goto('home.goals.confirm_delete_day')        

    def on_save_changes(self) -> None:
        self._oes.save_changes()
