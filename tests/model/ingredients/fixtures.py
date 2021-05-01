import model
import persistence


def get_honey() -> 'model.ingredients.Ingredient':
    return persistence.load(
        cls=model.ingredients.Ingredient,
        unique_value="Honey"
    )


def get_undefined_honey_quantity() -> 'model.ingredients.IngredientQuantityOf':
    return model.ingredients.IngredientQuantityOf(ingredient=get_honey())



def get_10g_of_honey() -> 'model.ingredients.IngredientQuantityOf':
    return model.ingredients.IngredientQuantityOf(
        ingredient=get_honey(),
        quantity_in_g=10
    )
