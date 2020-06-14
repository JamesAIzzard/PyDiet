from pyconsoleapp import ConsoleAppComponent

_MAIN = '''{plan_name}:

1. Breakfast            | 30-30-40 | 800cals
2. Lunch                | 30-30-40 | 1200cals
3. Dinner               | 30-30-40 | 1600cals

(a)  -- Add a meal.
(e*) -- Edit a meal.
(d*) -- Delete a meal.
(m)  -- Manage day micronutrient targets.

'''

class DayPlanEditorComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)