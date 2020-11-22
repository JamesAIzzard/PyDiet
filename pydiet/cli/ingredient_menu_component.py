from typing import Optional, TYPE_CHECKING

from pydiet import cli, ingredients
from pydiet.cli import BaseCreateEditDeleteComponent

if TYPE_CHECKING:
    from pydiet.cli import IngredientEditorComponent, IngredientSearchComponent


class IngredientMenuComponent(BaseCreateEditDeleteComponent):
    """Create/Edit/View/Delete menu for ingredients."""

    def __init__(self, **kwds):
        super().__init__(**kwds)
        self._subject_type_name = 'Ingredient'
        self._subject_type = ingredients.Ingredient
        self._subject_editor_route = 'home.ingredients.edit'
        self._editor_component: Optional['IngredientEditorComponent'] = None
        self._search_component: 'IngredientSearchComponent' = self.delegate_state(
            state='search', component_class=cli.IngredientSearchComponent)
        self._search_component.configure(subject_type_name=self._subject_type_name)

    def on_first_load(self) -> None:
        self._editor_component = self.app.get_component(cli.IngredientEditorComponent,
                                                        route=self._subject_editor_route, state='main')
