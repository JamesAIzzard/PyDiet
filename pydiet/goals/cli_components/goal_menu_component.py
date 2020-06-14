from pyconsoleapp import ConsoleAppComponent

_MAIN = '''Day Plans:

1. Training Day
2. Recovery Day
3. Rest Day
{day_plans}

(a)  -- Add day plan.
(e*) -- Edit day plan.
(d*) -- Delete day plan.
(m)  -- Manage overall micronutrient targets.

'''

class GoalMenuComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)