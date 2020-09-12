import abc, copy, enum
from pydiet import exceptions
from typing import TypedDict, Optional, cast

from pydiet import quantity, defining

class BulkTypes(str, enum.Enum):
    PIECE = 'piece'
    MASS = 'mass'
    VOLUME = 'volume'

class BulkData(TypedDict):
    pref_bulk_type: str  # 'pc', 'mass', 'vol'
    pref_mass_units: str  # Default mass units.
    g_per_ml: Optional[float]
    pref_vol_units: Optional[str]  # Default vol units.
    piece_mass_g: Optional[float]
    pref_piece_mass_units: Optional[str]  # Default pc mass units.

def get_empty_bulk_data() -> 'BulkData':
    return BulkData(
        pref_bulk_type=BulkTypes.MASS,
        pref_mass_units='g',
        g_per_ml=None,
        pref_vol_units=None,
        piece_mass_g=None,
        pref_piece_mass_units=None)

class SupportsBulk(defining.supports_name.SupportsName):

    @abc.abstractproperty
    def _bulk_data(self) -> 'BulkData':
        raise NotImplementedError

    @property
    def readonly_bulk_data(self) -> 'BulkData':
        return copy.deepcopy(self._bulk_data)

    @property
    def bulk_summary(self) -> str:

        # Preferred units:  L
        # Piece Mass:       180g
        # Density:          1kg/L (1g/ml)

        # Preferred units:  Undefined
        # Piece Mass:       Undefined
        # Density:          Undefined

        template = '''Preferred Units: {pref_units}
Piece Mass:      {piece_mass_summary}
Density:         {density_summary}
        '''

        pref_units = self.pref_bulk_units
        pc_mass_summary = 'Undefined'
        density_summary = 'Undefined'

        # Fill in placeholders'
        if self.piece_mass_defined:
            pc_mass_summary = '{pc_mass:.2f}{pc_mass_units}'.format(
                pc_mass=self.piece_mass_in_pref_units,
                pc_mass_units=self.pref_piece_mass_units
            )

        if self.density_is_defined:
            density_summary = '{dens_in_pref_units:.2f}{pref_mass_units}/{pref_vol_units} ({g_per_ml:.2f}g/ml)'.format(
                dens_in_pref_units=self.density_in_pref_units,
                pref_mass_units=self.pref_mass_units,
                pref_vol_units=self.pref_vol_units,
                g_per_ml=self.g_per_ml
            )

        # Return
        return template.format(
            pref_units=pref_units,
            piece_mass_summary=pc_mass_summary,
            density_summary=density_summary)

    @property
    def pref_bulk_type(self) -> 'BulkTypes':
        return self.classify_unit_to_bulk_type(self.pref_bulk_units)

    @property
    def pref_mass_units(self) -> str:
        return self.readonly_bulk_data['pref_mass_units']
    
    @property
    def g_per_ml(self) -> float:
        if not self.density_is_defined:
            raise quantity.exceptions.DensityDataUndefinedError
        return cast(float, self.readonly_bulk_data['g_per_ml'])

    @property
    def pref_vol_units(self) -> str:
        if not self.density_is_defined:
            raise quantity.exceptions.DensityDataUndefinedError
        return cast(str, self.readonly_bulk_data['pref_vol_units'])

    @property
    def piece_mass_g(self) -> float:
        if not self.piece_mass_defined:
            raise quantity.exceptions.PcMassDataUndefinedError
        return cast(float, self.readonly_bulk_data['pref_vol_units'])

    @property
    def pref_bulk_units(self) -> str:
        pref_bulk_type = self.readonly_bulk_data['pref_bulk_type']
        if pref_bulk_type == BulkTypes.MASS:
            return self.pref_mass_units
        elif pref_bulk_type == BulkTypes.VOLUME:
            return self.pref_vol_units
        elif pref_bulk_type == BulkTypes.PIECE:
            return BulkTypes.PIECE
        raise exceptions.PyDietException('Unknown bulk type.')

    @property
    def pref_piece_mass_units(self) -> str:
        if not self.piece_mass_defined:
            raise quantity.exceptions.PcMassDataUndefinedError
        return cast(str, self.readonly_bulk_data['pref_piece_mass_units'])

    @property
    def density_is_defined(self) -> bool:
        if self.readonly_bulk_data['g_per_ml'] == None or self.readonly_bulk_data['pref_vol_units'] == None:
            return False
        else:
            return True

    @property
    def piece_mass_defined(self) -> bool:
        if self.readonly_bulk_data['piece_mass_g'] == None or self.readonly_bulk_data['pref_piece_mass_units'] == None:
            return False
        else:
            return True

    @property
    def piece_mass_in_pref_units(self) -> float:
        if not self.piece_mass_defined:
            raise quantity.exceptions.PcMassDataUndefinedError
        return quantity.quantity_service.convert_mass_units(
            self.piece_mass_g, 'g', self.pref_piece_mass_units)

    @property
    def density_in_pref_units(self) -> float:

        # Convert 1g/ml into 1kg/L 

        k = (1/quantity.configs.G_CONVERSIONS[self.pref_mass_units])/\
            (1/quantity.configs.ML_CONVERSIONS[self.pref_vol_units])

        if not self.density_is_defined:
            raise quantity.exceptions.DensityDataUndefinedError
        return self.g_per_ml*k

    @property
    def pref_use_mass(self) -> bool:
        if self.pref_bulk_type == BulkTypes.MASS:
            return True
        else:
            return False

    @property
    def pref_use_volume(self) -> bool:
        if self.pref_bulk_type == BulkTypes.VOLUME:
            return True
        else:
            return False

    @property
    def pref_use_piece(self) -> bool:
        if self.pref_bulk_type == BulkTypes.PIECE:
            return True
        else:
            return False

    @property
    def grams_to_pref_units_ratio(self) -> float:
        return self.grams_to_other_units_ratio(self.pref_bulk_units)

    def grams_to_other_units_ratio(self, other_units:str)-> float:
        bulk_type = self.classify_unit_to_bulk_type(other_units)
        if bulk_type == BulkTypes.MASS:
            return 1/quantity.configs.G_CONVERSIONS[self.pref_mass_units]
        elif bulk_type == BulkTypes.VOLUME:
            return 1/quantity.configs.ML_CONVERSIONS[self.pref_vol_units]
        elif bulk_type == BulkTypes.PIECE:
            return 1/self.piece_mass_g
        else: raise exceptions.PyDietException('Unknown bulk type.')

    def classify_unit_to_bulk_type(self, unit:str) -> 'BulkTypes':
        unit = quantity.quantity_service.validate_qty_unit(unit)
        for bt in BulkTypes:
            if bt.value == self.readonly_bulk_data['pref_bulk_type']:
                return bt
        raise exceptions.PyDietException('Unknown bulk type.')

class SupportsBulkSetting(SupportsBulk):

    def set_pref_bulk_type(self, bulk_type:str) -> None:
        pass

    # TODO - Fill in the rest of the setters.
    #note I think it makes sense to do the validation here in this class
    # and have the abstract setter on the class simply write the data.
    # This keeps complexity out of the concrete classes, which is ultimately
    # what we want. 
