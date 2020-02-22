from pydiet.user_interface.views.view import View
from pydiet.services import services

class IngredientCostEditor(View):
    def __init__(self):
        self.weight = 0
        self.units = ''
        self.value = 0
        self.state = 'weight'

    @property
    def text(self):
        text = 'Example: [weight][units] costs £[value]\n'
        if self.state == 'weight':
            return text+'weight: '
        elif self.state == 'units':
            return text+'units: '
        elif self.state == 'value':
            return text+'value: '

    def response_action(self, res):
        if self.state == 'weight':
            self.weight = res
            self.state = 'units'
            return ''
        elif self.state == 'units':
            self.units = res
            self.state = 'value'
            return ''
        elif self.state == 'value':
            self.value = res
            services.ingredient.current_ingredient.set_price(
                float(self.value), float(self.weight), self.units
            )
            self.state = 'weight'
            return 'ingredient_editor'            

