from gui import configs
from gui.main import (
    set_noneable_qty_entry,
    get_noneable_qty_entry,
    validate_qty_entry,
    validate_nonzero_qty_entry,
    configure_qty_units,
    entry_is_defined)
from gui.base_controllers import BaseController, HasSubject, SupportsValidity, SupportsDefinition, AppPage
from gui.entry_widgets import SmartEntryWidget
from gui.smart_dropdown_widget import SmartDropdownWidget
from gui.scroll_frame_widget import ScrollFrameWidget
from gui.app import AppController, AppView
from gui.top_menu import TopMenuController, TopMenuView
from gui.bulk_editor import BulkEditorView, BulkEditorController
from gui.cost_editor import CostEditorView, CostEditorController
from gui.flag_nutrient_status import FlagNutrientStatusView, FlagNutrientStatusController
from gui.flag_editor import FlagEditorView, FlagEditorController
from gui.nutrient_editors import FixedNutrientRatiosEditorView, DynamicNutrientRatiosEditorView, \
    FixedNutrientRatiosEditorController, DynamicNutrientRatiosEditorController
from gui.nutrient_search import NutrientSearchView, NutrientSearchController
from gui.ingredient_editor import IngredientEditorController, IngredientEditorView
from gui.ingredient_search import IngredientSearchView, IngredientSearchController
from gui.recipe_editor import RecipeEditorView, RecipeEditorController

# Init the app;
app = AppController(
    view=AppView()
)
