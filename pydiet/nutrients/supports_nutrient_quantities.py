from pydiet import nutrients, quantity


class SupportsNutrientQuantities(nutrients.supports_nutrients.SupportsNutrients,
                                 quantity.supports_quantity.SupportsQuantity):

    ...
