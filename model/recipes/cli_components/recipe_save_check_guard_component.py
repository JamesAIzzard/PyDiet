import pydiet


class RecipeSaveCheckGuardComponent(pydiet.cli_components.BaseSaveCheckGuardComponent):

    def __init__(self, app):
        message = 'Save changes to this recipe?'
        super().__init__(message=message, app=app)
