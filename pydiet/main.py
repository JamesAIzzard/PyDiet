from pyconsoleapp import ConsoleApp

import pydiet
from pydiet import cli, nutrients

# Init the model;
nutrients.validation.validate_configs()
pydiet.build_flag_nutrient_rel_maps()
nutrients.build_global_nutrients()

# Init the app;
app: 'ConsoleApp' = ConsoleApp('PyDiet')
app.configure(routes={
    "home": cli.MainMenuComponent,
    "home.ingredients": cli.IngredientMenuComponent,
    # "home.ingredients.edit": cli.IngredientEditorComponent,
    # "home.ingredients.view": cli.IngredientViewerComponent,
    # "home.recipes": cli.RecipeMenuComponent,
    # "home.recipes.edit": cli.RecipeEditorComponent,
    # "home.recipes.view": cli.RecipeViewerComponent
})
app.current_route = 'home'
app.run()
