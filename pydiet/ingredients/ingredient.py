from pydiet.services import services

class Ingredient():
    def __init__(self, data):
        self._data = data

    @property
    def name(self):
        if not self._data['name'] == '':
            return self._data['name']

    @name.setter
    def name(self, value):
        self._data['name'] = value

    @property
    def cost_per_kg(self):
        conversion_factor = services.utils.convert_mass(
            self._data['cost_per_mass']['mass'], 
            self._data['cost_per_mass']['mass_units'], "kg"
        )
        return self._data['cost_per_mass']['cost']/conversion_factor

    @property
    def cost_summary(self):
        for key in self._data['cost_per_mass'].keys():
            if self._data['cost_per_mass'][key] == '':
                return None
        return '''{mass}{mass_units} costs approximately £{cost:.2f} (£{cost_per_kg:.2f}/kg)'''\
            .format(
                mass=self._data['cost_per_mass']['mass'],
                mass_units=self._data['cost_per_mass']['mass_units'],
                cost=self._data['cost_per_mass']['cost'],
                cost_per_kg=self.cost_per_kg
            )

    def set_price(self, cost, mass, mass_units):
        self._data['cost_per_mass']['cost'] = cost
        self._data['cost_per_mass']['mass'] = mass
        self._data['cost_per_mass']['mass_units'] = mass_units

    def summarise(self) -> str:
        return '''Mandatory Fields:
-----------------------------
Name: {name}
Cost: {cost}
'''.format(
            name=self.name,
            cost=self.cost_summary
        )
