from pyconsoleapp.builtin_components.yes_no_dialog_component import YesNoDialogComponent

from pydiet.optimisation import optimisation_edit_service as oes
from pydiet import repository_service as rep


class ConfirmDayGoalsDeleteComponent(YesNoDialogComponent):

    def __init__(self, app):
        super().__init__(app)
        self._oes = oes.OptimisationEditService()
        self.message = 'Are you sure you want to delete {dg_name}'.format(
            dg_name=self._oes.day_goals.unique_value)

    def on_yes(self):
        # If no datafile;
        if not self._oes.datafile_name:
            raise AttributeError
        # Set status message;
        self.app.info_message = '{dg_name} deleted.'.format(dg_name=self._oes.day_goals.unique_value)
        # Delete the datafile;
        rep.delete_day_goals_data(self._oes.datafile_name)
        # Clear instance and df name off the edit service;
        self._oes.datafile_name = None
        self._oes.day_goals = None
        # Redirect;
        self.app.goto('home.goals')

    def on_no(self):
        self.app.info_message = 'Day was not deleted.'
        self.app.goto('home.goals')