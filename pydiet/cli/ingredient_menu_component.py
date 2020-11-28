from typing import Optional, Type, TYPE_CHECKING

from pydiet import cli, ingredients
from pydiet.cli import BaseCreateEditDeleteComponent

if TYPE_CHECKING:
    from pydiet.persistence import SupportsPersistence
    from pydiet.cli import IngredientEditorComponent, IngredientSearchComponent


class IngredientMenuComponent(BaseCreateEditDeleteComponent):
    """Create/Edit/View/Delete menu for ingredients."""

    def __init__(self, **kwds):
        super().__init__(**kwds)

    @property
    def _subject_type(self) -> Type['SupportsPersistence']:
        return ingredients.Ingredient
