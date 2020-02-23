from pydiet.injector import injector


class Ingredient():
    def __init__(self, data):
        self._data = data

    @property
    def name(self):
        return self._data['name']

    @name.setter
    def name(self, value):
        self._data['name'] = value

    @property
    def cost_per_kg(self):
        for key in self._data['cost_per_mass']:
            if not self._data['cost_per_mass'][key]:
                return None
        conversion_factor = injector.utility_service.convert_mass(
            self._data['cost_per_mass']['mass'],
            self._data['cost_per_mass']['mass_units'], "kg"
        )
        return self._data['cost_per_mass']['cost']/conversion_factor

    @property
    def cost_summary(self):
        for key in self._data['cost_per_mass']:
            if not self._data['cost_per_mass'][key]:
                return None
        return '''{mass}{mass_units} costs approximately £{cost:.2f} (£{cost_per_kg:.2f}/kg)'''\
            .format(
                mass=self._data['cost_per_mass']['mass'],
                mass_units=self._data['cost_per_mass']['mass_units'],
                cost=self._data['cost_per_mass']['cost'],
                cost_per_kg=self.cost_per_kg
            )

    @property
    def flag_summary(self):
        summary = 'Flags: \n'
        for key in self._data['flags']:
            summary = summary+'- {flag}: {value}\n'\
                .format(flag=key, value=self.get_flag(key))
        return summary

    @property
    def mandatory_nutrient_data(self):
        data = {}
        for nutrient_name in injector.ingredient_service.MANDATORY_NUTRIENTS:
            data[nutrient_name] = self.get_nutrient_data(nutrient_name)
        return data

    @property
    def macronutrient_data(self):
        return self._data['macronutrients']

    @property
    def micronutrient_data(self):
        return self._data['micronutrients']

    @property
    def mandatory_nutrient_summary(self):
        return 'Mandatory Nutrients: \n'+self.multi_nutrient_summary(
            self.mandatory_nutrient_data
        )

    @property
    def macronutrient_summary(self):
        return 'Macronutrients: \n'+self.multi_nutrient_summary(
            self.macronutrient_data
        )

    @property
    def micronutrient_summary(self):
        return 'Micronutrients: \n'+self.multi_nutrient_summary(
            self.micronutrient_data
        )

    def nutrient_is_defined(self, nutrient):
        for field in nutrient.keys():
            if not nutrient[field]:
                return False
            else:
                return True

    def multi_nutrient_summary(self, nutrient_group):
        summary = ''
        for nutrient_name in nutrient_group.keys():
            if self.nutrient_is_defined(nutrient_group[nutrient_name]):
                summary = summary+'- '+nutrient_name+': '+self.nutrient_summary(nutrient_name)+'\n'
            else:
                summary = summary+'- '+nutrient_name+': None\n'
        return summary
                    

    def set_cost(self, cost, mass, mass_units):
        self._data['cost_per_mass']['cost'] = cost
        self._data['cost_per_mass']['mass'] = mass
        self._data['cost_per_mass']['mass_units'] = mass_units

    def get_flag(self, flag_name):
        return self._data['flags'][flag_name]

    def get_nutrient_data(self, nutrient_name):
        nutrients = {}
        nutrients.update(self._data['macronutrient_totals'])
        nutrients.update(self._data['macronutrients'])
        nutrients.update(self._data['micronutrients'])
        if nutrient_name in nutrients.keys():
            return nutrients[nutrient_name]

    def get_nutrient_percent(self, nutrient_name):
        data = self.get_nutrient_data(nutrient_name)
        if data:
            nutrient_mass_in_grams = injector.utility_service.convert_mass(
                data['mass'], data['mass_units'], 'g'
            )
            sample_mass_in_grams = injector.utility_service.convert_mass(
                data['mass_per'], data['mass_per_units'], 'g'
            )
            return (nutrient_mass_in_grams/sample_mass_in_grams)*100

    def nutrient_summary(self, nutrient_name):
        data = self.get_nutrient_data(nutrient_name)
        if data:
            summary = '''{sample_mass}{sample_mass_units} {ingredient_name}: {nutrient_mass}{nutrient_mass_units} {nutrient_name}'''\
                .format(
                    sample_mass=data['mass_per'],
                    sample_mass_units=data['mass_per_units'],
                    ingredient_name=self.name,
                    nutrient_mass=data['mass'],
                    nutrient_mass_units=data['mass_units'],
                    nutrient_name=nutrient_name
                )
            return summary

    @property
    def summary(self):
        summary = '''
-------------- Mandatory Info --------------

Name: {name}
Cost: {cost}

{flags}

{mand_nutrients}

------------ All Macronutrients ------------
{all_macros}

------------ All Micronutrients ------------
{all_micros}

'''.format(
            name=self.name,
            cost=self.cost_summary,
            flags=self.flag_summary,
            mand_nutrients=self.mandatory_nutrient_summary,
            all_macros=self.macronutrient_summary,
            all_micros=self.micronutrient_summary
        )
        return summary
