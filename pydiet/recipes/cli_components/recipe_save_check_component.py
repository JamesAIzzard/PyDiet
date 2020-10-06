from pyconsoleapp import builtin_components, ConsoleAppGuardComponent

class RecipeSaveCheckComponent(builtin_components.yes_no_dialog_component.YesNoDialogComponent,
                               ConsoleAppGuardComponent):

    def __init__(self, app):
        super().__init__(app)
        self._message = 'Save changes ot this ingredient?'
        self._ingredient