from pyconsoleapp import ConsoleApp

app = ConsoleApp('PyDiet')

app.register_component_package('pydiet.cli.components')
app.register_component_package('pydiet.cli.components.ingredients')
app.register_component_package('pydiet.cli.components.ingredients.flags')
app.register_component_package('pydiet.cli.components.ingredients.cost')
app.register_component_package('pydiet.cli.components.ingredients.nutrient')

app.add_root_route(['home'], 'MainMenu')
app.add_route(['home', 'ingredients'], 'IngredientMenu')
app.add_route(['home', 'ingredients', 'new'], 'IngredientEditMenu')
app.add_route(['home', 'ingredients', 'new', 'name'], 'IngredientNameEditor')
app.add_route(['home', 'ingredients', 'new', 'flags'], 'IngredientFlagMenu')
app.add_route(['home', 'ingredients', 'new', 'flags', 'set_all?'], 'CycleIngredientFlagsQuestion')
app.add_route(['home', 'ingredients', 'new', 'flags', 'set'], 'SetFlag')
app.add_route(['home', 'ingredients', 'new', 'flags', 'flags_are_set'], 'FlagsAreSet')
app.add_route(['home', 'ingredients', 'new', 'cost_mass'], 'SetCostMass')
app.add_route(['home', 'ingredients', 'new', 'cost'], 'SetCost')
app.add_route(['home', 'ingredients', 'new', 'macro_totals'], 'MacroTotalsMenu')
app.add_route(['home', 'ingredients', 'new', 'macro_totals', 'sample_mass'], 'NutrientPerMass')
app.add_route(['home', 'ingredients', 'new', 'macro_totals', 'nutrient_mass'], 'NutrientMass')