from pyconsoleapp import ConsoleApp

from pydiet import cli

app: 'ConsoleApp' = ConsoleApp('PyDiet')

app.configure(routes={
    "home": cli.MainMenuComponent,
    "home.ingredients": cli.IngredientMenuComponent,
    "home.ingredients.edit": cli.IngredientEditorComponent,
    "home.ingredients.view": cli.IngredientViewerComponent,
    "home.recipes": cli.RecipeMenuComponent,
    "home.recipes.edit": cli.RecipeEditorComponent,
    "home.recipes.view": cli.RecipeViewerComponent
})

app.current_route = 'home'
