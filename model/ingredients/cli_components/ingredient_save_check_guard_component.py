import pydiet


class IngredientSaveCheckGuardComponent(pydiet.cli_components.BaseSaveCheckGuardComponent):

    def __init__(self, app):
        message = 'Save changes to this ingredient?'
        super().__init__(message=message, app=app)
