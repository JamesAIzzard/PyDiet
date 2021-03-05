from typing import TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent

from pydiet import nutrients, tags, flags

if TYPE_CHECKING:
    from pydiet.optimisation.meal_goals import MealGoals

_TEMPLATE = '''
-save, -s     -> Save changes.
-----------------------------------------------
General:
-name, -n    [name]            | {name}
-time, -t    [serve time]      | {time}
-cost, -m    [max cost]        | £{max_cost}
-----------------------------------------------
Basic Composition:
-fat, -f     [perc fat]        | {perc_fat}
-carbs, -c   [perc carbs]      | {perc_carbs}
-protein, -p [perc protein]    | {perc_prot}
-pcals       [perc total cals] | {perc_total_cals}
-cals        [total cals]      | {total_cals}
-----------------------------------------------
Custom Nutrients: 
1. Sodium - 200mg
{custom_nutrient_menu}

-nuts -> Edit nutrient targets.
-----------------------------------------------
Tags:
1. main
2. savory
3. drink
{tag_menu}

-comps -> Edit meal tags.
------------------------------------------------

Flags:
1. alcohol-free
{flag_menu}

-flag_data -> Edit flag_data.
'''

class MealGoalsEditorComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self.subject:'MealGoals'
        self.set_print_function(self.print)
        self.set_response_function(['-save', '-s'], self.on_save_changes)

    @property
    def custom_nutrient_menu(self)->str:
        raise NotImplementedError

    @property
    def component_menu(self)->str:
        raise NotImplementedError

    @property
    def flag_menu(self)->str:
        raise NotImplementedError

    def print(self)->str:
        # Build the template;
        output = _TEMPLATE.format(
            name=self.subject.unique_value,
            time=self.subject.time,
            max_cost=self.subject.max_cost_gbp,
            perc_fat=self.subject.perc_fat,
            perc_carbs=self.subject.perc_carbs,
            perc_prot=self.subject.perc_protein,
            perc_total_cals=self.subject.perc_of_day_cals,
            total_cals=self.subject.calories,
            custom_nutrient_menu=nutrients.print_nutrient_targets_menu(self.subject),
            tag_menu=tags.print_enumerated_active_tags(self.subject),
            flag_menu=flags.print_active_flags_menu(self.subject)
        )
        
        # Frame it in the standard page;
        output = self.app.fetch_component('standard_page_component').call_print(
            page_title='Meal Goals Editor', page_content=output)

        return output

    def on_save_changes(self):
        raise NotImplementedError