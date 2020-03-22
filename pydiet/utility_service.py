
from typing import Tuple

g_conversions = {
    "ug": 1e-6,  # 1 microgram = 0.000001 grams
    "mg": 1e-3,  # 1 milligram = 0.001 grams
    "g": 1,  # 1 gram = 1 gram! :)
    "kg": 1e3,  # 1 kilogram = 1000 grams
}


class UtilityService():

    @property
    def recognised_units(self):
        return g_conversions.keys()

    @staticmethod
    def convert_mass(mass: float, start_units: str, end_units: str) -> float:
        # Convert value to grams first
        mass_in_g = g_conversions[start_units]*mass
        return mass_in_g/g_conversions[end_units]

    @staticmethod
    def sentence_case(text: str) -> str:
        '''Capitalizes the first letter of each word in the
        text provided.

        Args:
            text (str): Text to convert to sentence case.

        Returns:
            str: Text with sentence case capitalisation.
        '''
        words_list = text.split('_')
        for word in words_list:
            word.capitalize()
        return ' '.join(words_list)

    def parse_mass_and_units(self, mass_and_units: str) -> Tuple[float, str]:
        output = None
        # Strip any initial whitespace;
        mass_and_units = mass_and_units.replace(' ', '')
        # Work along the string until you find something which is
        # not a number;
        for i, char in enumerate(mass_and_units):
            # If char cannot be parsed as a number,
            # split the string here;
            if not char.isnumeric() and not char == '.':
                mass_part = float(mass_and_units[:i])
                units_part = str(mass_and_units[i:])
                output = (mass_part, units_part)
                break
        if not output:
            raise ValueError('Unable to parse {} into a mass and unit.'
                             .format(mass_and_units))
        # Check that the units are recognised;
        if output[1] not in self.recognised_units:
            raise ValueError('{} is not a recognised mass unit.'\
                .format(output[1]))
        # Return tuple;
        return output
