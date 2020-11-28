from pydiet import cli, ingredients


class IngredientSearchComponent(cli.BaseSearchComponent):
    """Component to implement searching and selecting ingredients."""

    def __init__(self, **kwds):
        super().__init__(subject_type=ingredients.Ingredient, **kwds)

    @property
    def _subject_type(self):
