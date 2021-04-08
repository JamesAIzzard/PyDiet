import tkinter as tk
from typing import Dict, Optional

import gui
import model


class FixedNutrientRatiosEditorWidget(tk.Frame):
    """Widget to allow manipulation of a fixed collection of nutrient ratios."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._nutrient_ratio_widgets: Dict[str, 'gui.NutrientRatioEditorWidget'] = {}

    def add_nutrient_ratio_widget(self, nutrient_name: str) -> None:
        """Adds a nutrient ratio widget to the UI."""
        if nutrient_name not in self._nutrient_ratio_widgets.keys():
            self._nutrient_ratio_widgets[nutrient_name] = gui.NutrientRatioEditorWidget(
                master=self,
                nutrient_name=nutrient_name
            )
            self._nutrient_ratio_widgets[nutrient_name].pack()


class FixedNutrientRatiosEditorController:
    """Controller for FixedNutrientRatiosEditorWidget."""

    # What methods do we need here?
    # How is validation going to work?
    # Probably, once the user presses save, the software will go ahead and
    # try to push the data into the ingredient, at which point, any issues
    # will emerge.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._subject: Optional['model.nutrients.HasSettableNutrientRatios'] = None

    @property
    def subject(self) -> 'model.nutrients.HasSettableNutrientRatios':
        """Returns the subject."""
        return self._subject

    @subject.setter
    def subject(self, subject: 'model.nutrients.HasSettableNutrientRatios'):
        """Sets the subject."""
        if not isinstance(subject, model.nutrients.HasSettableNutrientRatios):
            raise TypeError("Subject must implement HasSettableNutrientRatios.")
        self._subject = subject

    @property
    def nutrient_ratios(self) -> Dict[str, Dict]:
        """Seems like we shouldn't try and do too much conversion work here. Instead,
        just pass the data straight out of the UI and make sure the model has the
        appropriate methods to set based on that data.
        """
