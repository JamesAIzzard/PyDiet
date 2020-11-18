from pyconsoleapp import Component, PrimaryArg
from pyconsoleapp.builtin_components import StandardPageComponent


class MainMenuComponent(Component):
    _template = u'''-ingr \u2502 -> Manage system ingredients.
-recp \u2502 -> Manage system recipes.
-goal \u2502 -> Manage system goals.
-solv \u2502 -> Generate meal plans.
-view \u2502 -> View meal plans.
'''

    def __init__(self, **kwds):
        super().__init__(**kwds)
        self.configure(responders=[
            self.configure_responder(self._on_manage_ingredients, args=[
                PrimaryArg(name='ingredients_flag', accepts_value=False, markers=['-ingr'])
            ])
        ])
        self._page_component = self.use_component(StandardPageComponent)
        self._page_component.configure(page_title='Main Menu')

    def printer(self, **kwds) -> str:
        return self._page_component.printer(page_content=self._template)

    def _on_manage_ingredients(self):
        self.app.go_to('home.ingredients')
