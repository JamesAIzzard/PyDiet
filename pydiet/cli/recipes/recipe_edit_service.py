from typing import TYPE_CHECKING, Optional

from pinjector import inject

if TYPE_CHECKING:
    from pydiet.recipes.recipe import Recipe


class RecipeEditService():

    def __init__(self):
        self.recipe: Optional['Recipe']
        self.datafile_name:Optional[str]
