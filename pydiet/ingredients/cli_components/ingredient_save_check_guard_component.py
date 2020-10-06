from typing import Optional, TYPE_CHECKING

import pydiet

if TYPE_CHECKING:
    from pydiet.ingredients.ingredient import Ingredient


class IngredientSaveCheckGuardComponent(pydiet.cli_components.BaseSaveCheckGuardComponent):

    def __init__(self, app):
        message = 'Save changes to this ingredient?'
        super().__init__(message=message, app=app)
        self._subject: Optional['Ingredient'] = None

    def configure(self, subject: 'Ingredient') -> None:
        super()._configure(subject=subject)
