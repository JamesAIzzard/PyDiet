from typing import Optional, Type, TYPE_CHECKING

from pydiet import cli, ingredients
from pydiet.cli import BaseCreateEditDeleteComponent

if TYPE_CHECKING:
    from pydiet.persistence import SupportsPersistence
    from pydiet.cli import IngredientEditorComponent, IngredientSearchComponent


class IngredientMenuComponent(BaseCreateEditDeleteComponent):
    """Create/Edit/View/Delete menu for ingredients."""

    _subject_type: Type['SupportsPersistence'] = ingredients.Ingredient
    _subject_type_name: str = 'Ingredient'

    def __init__(self, editor_component: 'IngredientEditorComponent',
                 search_component: 'IngredientSearchComponent', **kwds):
        super().__init__(editor_component=editor_component, search_component=search_component, **kwds)
