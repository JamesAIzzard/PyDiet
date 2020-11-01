from typing import Optional, TYPE_CHECKING

from pyconsoleapp import Component

from pydiet import cli, persistence

if TYPE_CHECKING:
    from pydiet import Ingredient

_menu_screen_template = '''
Ingredient Status: {status_summary}

Name: {name}
Cost: {cost}

Bulk (Weight & Density):
{bulk_summary}

Flags:
{flags_summary}

Nutrients:     
{nutrients_summary}

{single_hr}
-ok     \u2502 -> -OK & save.
-cancel \u2502 -> Cancel.
{single_hr}
-name [name]            \u2502 -> Set the ingredient name.
-cost [cost] -per [qty] \u2502 -> Set the ingredient cost.
-bulk                   \u2502 -> Edit the ingredient's weight and density.
-flags                  \u2502 -> Edit the ingredient's flags.
-nutr                   \u2502 -> Edit the ingredient's nutrients.
{single_hr}
'''


class IngredientEditorComponent(Component):
    def __init__(self, **kwds):
        super().__init__(**kwds)

        self.configure(responders=[
            self.configure_responder()
        ])

        self._bulk_editor = self.delegate_state('edit_bulk', cli.BulkEditorComponent)
        self._flag_editor = self.delegate_state('edit_flags', cli.FlagEditorComponent)
        self._nutrient_editor = self.delegate_state('edit_nutrients', cli.NutrientEditorComponent)

        self._ingredient: Optional['Ingredient'] = None

    def on_load(self) -> None:
        self._bulk_editor.configure(subject=self._ingredient, state='main')
        self._flag_editor.configure(subject=self._ingredient, state='main')
        self._nutrient_editor.configure(subject=self._ingredient, state='main')

    def _on_ok_and_save(self) -> None:
        persistence.save(self._ingredient)
        self.app.go_to('home.ingredients')

    def _on_cancel(self) -> None:
        self.app.go_to('home.ingredients')

    def _on_set_name(self, name: str) -> None:
        self._ingredient.name = name

    def _on_set_cost(self, cost_gbp: float, cost_qty: float, cost_qty_unit: float) -> None:
        self._ingredient.set_cost(cost_gbp=cost_gbp, qty=cost_qty, unit=cost_qty_unit)

    def _on_edit_bulk(self) -> None:
        self.current_state = 'edit_bulk'
