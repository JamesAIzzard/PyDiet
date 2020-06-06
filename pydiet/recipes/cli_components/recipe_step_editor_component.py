from pyconsoleapp import ConsoleAppComponent

from pydiet.recipes import recipe_edit_service as res

_TEMPLATE = '''Edit Step {step_number}:
------------------
Enter the step instructions, and press (enter).

'''


class RecipeStepEditorComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app)
        self._res = res.RecipeEditService()

    def print(self):
        # Build the step number:
        ## If we are adding a new step;
        if self._res.selected_step_number == None:
            step_number = len(self._res.recipe.steps)+1
        ## If we are editing a step;
        else:
            step_number = self._res.selected_step_number
        # Build the output;
        output = _TEMPLATE.format(step_number=step_number)
        output = self.app.fetch_component('standard_page_component').print(output) 
        # No prefill if adding new;
        if self._res.selected_step_number == None:
            return output
        # Add prefill if editing;
        else:
            return output, self._res.recipe.steps[str(self._res.selected_step_number)] 

    def dynamic_response(self, raw_response: str) -> None:
        # If we are adding a new step;
        if self._res.selected_step_number == None:
            # Take the input and append it to the step list;
            self._res.recipe.append_step(raw_response)
            # Redirect to the step editor page;
        # If we are editing an existing step;
        else:
            # Update the step;
            self._res.recipe.steps[str(self._res.selected_step_number)] = raw_response
            # Deselect the step;
            self._res.selected_step_number = None
        # Redirect back to step menu;
        self.app.goto('..')
