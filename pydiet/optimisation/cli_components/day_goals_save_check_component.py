from pyconsoleapp import ConsoleAppGuardComponent
from pyconsoleapp.builtin_components.yes_no_dialog_component import YesNoDialogComponent

from pydiet.optimisation.exceptions import (
    DayGoalsNameUndefinedError
)
from pydiet.optimisation import optimisation_edit_service as oes

class DayGoalsSaveCheckComponent(YesNoDialogComponent, ConsoleAppGuardComponent):

    def __init__(self, app):
        super().__init__(app)
        self._oes = oes.OptimisationEditService()
        self.message = 'Save changes to these day goals?'

    def on_yes(self):
        # Try and save;
        try:
            self._res.save_changes()
            # Clear the exit guard;
            self.clear_self()
        # If the day_goals were unnamed;
        except DayGoalsNameUndefinedError:
            # Tell the user;
            self.app.info_message = 'Day goals must be named before they can be saved.'
            # Reverse;
            self.app.back()

    def on_no(self):
        # Confirm;
        self.app.info_message = 'Day goals not saved.'
        # Clear the exit guard;
        self.clear_self()