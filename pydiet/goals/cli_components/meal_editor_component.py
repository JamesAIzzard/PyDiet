from pyconsoleapp import ConsoleAppComponent

_MAIN = '''Meal Description:

(s)    -- Save changes.
-----------------------------------------------
General:
(n-*)  -- Name         | {name}
(t-*)  -- Time         | {time}
(m-*)  -- Max Cost     | {max_cost}
-----------------------------------------------
Basic Composition:
(f-*)  -- % Fat        | {perc_fat}
(c-*)  -- % Carbs      | {perc_carbs}
(p-*)  -- % Protein    | {perc_prot}
(t-*)  -- % Total Cals | {perc_tot_cals}
-----------------------------------------------

(ac-*) -- Add components.
(rc-*) -- Remove component *.

Current Components:
1. main
2. savory
3. drink
{current_components}

Available Components:
1. side
2. sweet
3. savory
4. snack

Flags:
1. alcohol-free
(af-*)  -- Add flag.
(rf-*)  -- Remove flag.

'''

class MealEditorComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self.set_option_response('s', self.on_save_changes)

    def on_save_changes(self):
        raise NotImplementedError