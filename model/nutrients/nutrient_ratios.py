import abc
from typing import Dict, List, Any, Optional, TypedDict

import model
import persistence


class NutrientRatioData(TypedDict):
    """Persisted data format for NutrientRatio instances."""
    nutrient_g_per_subject_g: Optional[float]
    nutrient_pref_units: str


NutrientRatiosData = Dict[str, 'NutrientRatioData']


class NutrientRatio(model.SupportsDefinition, model.HasName, persistence.CanLoadData):
    """Models an amount of nutrient per substance."""

    def __init__(self, nutrient_name: str, nutrient_ratio_data: Optional['NutrientRatioData'] = None, **kwargs):
        super().__init__(**kwargs)
        # Make sure we are using the primary name;
        nutrient_name = model.nutrients.get_nutrient_primary_name(nutrient_name)
        # Grab a reference to the associated nutrient;
        self._nutrient: 'model.nutrients.Nutrient' = model.nutrients.GLOBAL_NUTRIENTS[nutrient_name]

        # Create somewhere to stash the instance data;
        self._nutrient_ratio_data: 'NutrientRatioData' = NutrientRatioData(
            nutrient_g_per_subject_g=None,
            nutrient_pref_units='g'
        )

        # If data was provided, go ahead and load it;
        if nutrient_ratio_data is not None:
            self.load_data(nutrient_ratio_data)

    def _get_name(self) -> Optional[str]:
        return self.nutrient.primary_name

    @property
    def nutrient(self) -> 'model.nutrients.Nutrient':
        """Returns the nutrient associated with the nutrient ratio."""
        return self._nutrient

    @property
    def g_per_subject_g(self) -> Optional[float]:
        """Returns the grams of the nutrient per gram of subject."""
        if self._nutrient_ratio_data['nutrient_g_per_subject_g'] is None:
            raise model.nutrients.exceptions.UndefinedNutrientRatioError(
                subject=self,
                nutrient_name=self.nutrient.primary_name
            )
        else:
            return self._nutrient_ratio_data['nutrient_g_per_subject_g']

    @property
    def pref_unit(self) -> str:
        """Returns the preferred unit used to refer to the nutrient quantity on this instance."""
        return self._nutrient_ratio_data['nutrient_pref_units']

    @property
    def mass_in_pref_unit_per_subject_g(self) -> float:
        """Returns the mass of nutrient in its pref units, per gram of subject."""
        return model.quantity.convert_qty_unit(
            qty=self.g_per_subject_g,
            start_unit='g',
            end_unit=self.pref_unit
        )

    @property
    def is_defined(self) -> bool:
        """Returns True/False to indicate if the nutrient ratio is fully defined."""
        return self._nutrient_ratio_data['nutrient_g_per_subject_g'] is not None

    @property
    def is_zero(self) -> bool:
        """Returns True/False to indicate if the nutrient ratio is explicitly set to zero."""
        return self.g_per_subject_g == 0

    @property
    def is_non_zero(self) -> bool:
        """Returns True/False to indicate if the nutrient ratio is not zero."""
        return not self.is_zero

    def load_data(self, nutrient_ratio_data: 'NutrientRatioData', **kwargs) -> None:
        self._nutrient_ratio_data = nutrient_ratio_data

    @property
    def persistable_data(self) -> Dict[str, Any]:
        return self._nutrient_ratio_data


class SettableNutrientRatio(NutrientRatio):
    """Models a settable nutrient ratio. Careful where you return these! Nutrient ratios
    shouldn't be set without mutually validating all nutrients on the subject.
    Notes:
        It is was quite tempting to create a "smarter" setter method on this class, which could be
        passed nutrient quantities and subject quantities in any units, and figure out what the
        basic ratio was before setting it. However, this requires knowledge of the units configured
        on the subject, which would mean passing density and pc mass in. This is possible, but on
        balance didn't seem worth it. Additionally, nutrient ratio data should always be set through
        the subject anyway, because the nutrient family validation process needs to be carried out.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Check that we don't have readonly flag_data (this would allow inconsistencies);
        if not isinstance(self, model.flags.HasSettableFlags):
            assert not isinstance(self, model.flags.HasFlags)

    @NutrientRatio.g_per_subject_g.setter
    def g_per_subject_g(self, g_per_subject_g: Optional[float]) -> None:
        """Implementation for setting grams of nutrient per gram of subject.
        Note:
            This method is not responsible for mutual validation of the set of nutrient ratios
            which may be on the instance. Their mutual validity must be maintained by the instance
            on which they exist.
        """
        if g_per_subject_g is not None:
            self._nutrient_ratio_data['nutrient_g_per_subject_g'] = model.quantity.validation.validate_quantity(g_per_subject_g)
        else:
            self._nutrient_ratio_data['nutrient_g_per_subject_g'] = None

    @NutrientRatio.pref_unit.setter
    def pref_unit(self, pref_mass_unit: str) -> None:
        """Impelmetnation for setting the pref_unit."""
        self._nutrient_ratio_data['nutrient_pref_units'] = model.quantity.validation.validate_mass_unit(pref_mass_unit)

    def undefine(self) -> None:
        """Resets g_per_subject_g to None and pref_unit to 'g'."""
        self.g_per_subject_g = None
        self.pref_unit = 'g'

    def zero(self) -> None:
        """Zeroes the nutrient ratio."""
        self.g_per_subject_g = 0


class HasNutrientRatios(model.quantity.HasBulk, abc.ABC):
    """Abstract class to model objects with readonly nutrient ratios.
    Notes:
        This implementation assumes that only *defined* nutrient ratios are returned by
        the nutrient ratio method. This is useful for various reasons;
        1. We don't store instances which don't contain data.
        2. We don't pass empty fields to the persistence module.
        3. We can use Set mathematics to identify the differences between sets of nutrients, which amount
            to defined and undefined nutrients in certain categories.

        We don't put a constructor on this class because not all child classes which have nutrient ratios
        will store/define the data in the same way. For example, the Ingredient class will simply store
        a dictionary of (Settable)NutrientRatio while a recipe will just store a collection of Ingredient
        instances. Therefore, the way we obtain the nutrient ratios here will depend on the concrete
        implementation of the child class.
    """

    @property
    @abc.abstractmethod
    def nutrient_ratios(self) -> Dict[str, 'NutrientRatio']:
        """Returns all defined nutrient ratios keyed by their primary names.
        Notes:
            See class docstring; should only return defined instances.
            Also - since these are part of the public interface, they can only be non-settable!
        """
        raise NotImplementedError

    def get_nutrient_ratio(self, nutrient_name: str) -> 'NutrientRatio':
        """Returns a NutrientRatio by name."""
        # Convert to the primary name, in case we were given an alias;
        nutrient_name = model.nutrients.get_nutrient_primary_name(nutrient_name)
        # If the nutrient is defined (i.e if it is in the dictionary);
        if nutrient_name in self.nutrient_ratios.keys():
            # Return it;
            return self.nutrient_ratios[nutrient_name]
        # Otherwise, return an error to indicate it isn't defined;
        else:
            raise model.nutrients.exceptions.UndefinedNutrientRatioError(
                subject=self,
                nutrient_name=nutrient_name
            )

    def nutrient_ratio_is_defined(self, nutrient_name: str) -> bool:
        """Returns True/False to indiciate if the named nutrient ratio has been defined."""
        # Make sure we have the primary nutrient name;
        nutrient_name = model.nutrients.get_nutrient_primary_name(nutrient_name)
        # If it's in the dict, it is defined;
        return nutrient_name in self.nutrient_ratios.keys()

    @property
    def undefined_mandatory_nutrient_ratios(self) -> List[str]:
        """Returns a list of the mandatory nutrient ratios which are undefined."""
        return list(set(model.nutrients.configs.MANDATORY_NUTRIENT_NAMES).difference(set(self.nutrient_ratios.keys())))

    @property
    def defined_optional_nutrient_ratios(self) -> List[str]:
        """Returns a list of optional nutrient names which are defined."""
        return list(set(model.nutrients.OPTIONAL_NUTRIENT_NAMES).union(set(self.nutrient_ratios.keys())))

    def get_nutrient_mass_in_pref_unit_per_subject_ref_qty(self, nutrient_name: str) -> float:
        """Returns the mass of a nutrient in its preferred unit, per reference mass of the subject."""
        return self.get_nutrient_ratio(nutrient_name).mass_in_pref_unit_per_subject_g * self.g_in_ref_qty

    def validate_nutrient_ratio(self, nutrient_name: str) -> None:
        """Checks the named nutrient ratio against other defined nutrient ratios in its family.
        Notes
            Although we are dealing with ratios instead of masses, we can use the validate mass function
            here because all ratios are stored per nutrient gram. Therefore, effectively, all nutrient
            ratios per gram of ingredient can represent an absolute mass of the nutrient, for the purpose
            of validation here.
        """

        # We need to make a small tweak to the get_nutrient_ratio method, to make it raise the correct exception
        # here, so it works with the mass validator function. I suppose another approach would be to generalise
        # the validator function a little, but this way should work fine;
        def get_nutrient_mass_g(nutr_name: str) -> float:
            try:
                return self.get_nutrient_ratio(nutr_name).g_per_subject_g
            except model.nutrients.exceptions.UndefinedNutrientRatioError:
                raise model.nutrients.exceptions.UndefinedNutrientMassError(
                    subject=self,
                    nutrient_name=nutr_name
                )

        # Call the validator function, passing in our tweaked getter;
        model.nutrients.validate_nutrient_family_masses(
            nutrient_name=nutrient_name,
            get_nutrient_mass_g=get_nutrient_mass_g
        )


class HasSettableNutrientRatios(HasNutrientRatios, persistence.CanLoadData, abc.ABC):
    """Abstract class to model objects with settable nutrient ratios.
    Notes:
        To make sure any changes to NutrientRatio instances pass through the family validation
        process, its important not to give out SettableNutrientRatio instances. All changes to nutrient
        ratios must be implemented through this class' methods.

        All classes which have SettableNutrientRatios also store them locally, so we can add a
        constructor here, with a local dictionary to store the data. Also, since we now know the
        instance is storing data locally, we can also inherit from HasPersistableData, and provide
        concrete implementations of its methods to get data into and out of the instance.
    """

    def __init__(self, nutrient_ratios_data: Optional[Dict[str, 'NutrientRatioData']] = None, **kwargs):
        super().__init__(**kwargs)

        # Create somewhere to store the data;
        self._nutrient_ratios: Dict[str, 'SettableNutrientRatio'] = {}

        # If we got data, then load it up;
        if nutrient_ratios_data is not None:
            self.load_data({'nutrient_ratios_data': nutrient_ratios_data})

    @property
    def nutrient_ratios(self) -> Dict[str, 'NutrientRatio']:
        # We need to convert these to readonly versions, to do nutrient family validation,  writing must take
        # place through this class' methods - so don't give out writeable versions.
        # First, create somewhere to store the new readonly versions;
        _nutrient_ratios: Dict[str, 'NutrientRatio'] = {}
        # Next, work the dict and convert the writable NutrientRatio instances into readonly versions;
        for nutrient_name, settable_nutrient_ratio in self._nutrient_ratios.items():
            _nutrient_ratios[nutrient_name] = NutrientRatio(
                nutrient_name=nutrient_name,
                nutrient_ratio_data=settable_nutrient_ratio.persistable_data
            )
        # Now, return the dict of reaodnly instances;
        return _nutrient_ratios

    def _get_settable_nutrient_ratio(self, nutrient_name: str) -> 'SettableNutrientRatio':
        """Returns a SettableNutrientRatio instance. IMPORTANT! Internal use only - see class docstring."""
        # Make sure we are dealing with the primary version of the nutrient name.
        nutrient_name = model.nutrients.get_nutrient_primary_name(nutrient_name)

        # If we have this nutrient defined;
        if nutrient_name in self._nutrient_ratios.keys():
            return self._nutrient_ratios[nutrient_name]
        else:
            raise model.nutrients.exceptions.UndefinedNutrientRatioError(
                nutrient_name=nutrient_name,
                subject=self
            )

    def set_nutrient_ratio(self, nutrient_name: str,
                           nutrient_qty: Optional[float],
                           nutrient_qty_unit: str,
                           subject_qty: float,
                           subject_qty_unit: str) -> None:
        """Sets the data on the named nutrient ratio, and runs family validation."""

        # Catch zero subject quantity;
        if subject_qty == 0:
            raise model.quantity.exceptions.ZeroQtyError(subject=self)

        # Make sure we are dealing with the nutrient's primary name;
        nutrient_name = model.nutrients.get_nutrient_primary_name(nutrient_name)

        # We can't break anything if we are unsetting the nutrient, so just go ahead and do it and skip the rest;
        if nutrient_qty is None:
            del self._nutrient_ratios[nutrient_name]
            return

        # Take a backup, in case the change breaks something;
        # Since this converts our SettableNutrientRatio into a NutrientRatio, we get a whole new instance,
        # so its OK to use it as a backup - its independent of the version we are about to mess with;
        try:
            backup_nutrient_ratio = self.get_nutrient_ratio(nutrient_name)
        except model.nutrients.exceptions.UndefinedNutrientRatioError:
            # Ahh OK, this one wasn't defined yet, just set the backup to None;
            backup_nutrient_ratio = None

        # Grab the settable nutrient ratio instance;
        try:
            master_nutrient_ratio = self._get_settable_nutrient_ratio(nutrient_name)
        except model.nutrients.exceptions.UndefinedNutrientRatioError:
            # OK, we don't have this one yet. Create it;
            self._nutrient_ratios[nutrient_name] = model.nutrients.SettableNutrientRatio(nutrient_name=nutrient_name)
            master_nutrient_ratio = self._get_settable_nutrient_ratio(nutrient_name)

        # OK, I need to work out what the base ratio is, from the information which was passed in;
        # Start by putting the nutrient quantity into grams;
        try:
            nutrient_qty_g = model.quantity.convert_qty_unit(
                qty=nutrient_qty,
                start_unit=nutrient_qty_unit,
                end_unit='g'
            )  # No need to consider any special units here, we only allow mass.
        # If the nutrient quantity unit was something wierd which was not a mass, then convert the exception
        # to indicate that the unit type was wrong;
        except model.quantity.exceptions.UnitNotConfiguredError:
            raise model.quantity.exceptions.IncorrectUnitTypeError(
                subject=self,
                unit=nutrient_qty_unit
            )

        # Nice, next step is to get the subject quantity into grams;
        subject_qty_g = model.quantity.convert_qty_unit(
            qty=subject_qty,
            start_unit=subject_qty_unit,
            end_unit='g',
            g_per_ml=self.g_per_ml if self.density_is_defined else None,
            piece_mass_g=self.piece_mass_g if self.piece_mass_defined else None
        )

        # Quickly check the nutrient quantity doesn't exceed the subject quantity;
        if nutrient_qty_g > subject_qty_g * 1.001:
            raise model.nutrients.exceptions.NutrientQtyExceedsSubjectQtyError(
                subject=self,
                nutrient_name=nutrient_name,
                nutrient_qty=nutrient_qty,
                nutrient_qty_units=nutrient_qty_unit,
                subject_qty=subject_qty,
                subject_qty_units=subject_qty_unit
            )

        # Now ahead and make the change;
        master_nutrient_ratio.g_per_subject_g = nutrient_qty_g / subject_qty_g
        master_nutrient_ratio.pref_unit = nutrient_qty_unit

        # Final step is to run the validation;
        try:
            self.validate_nutrient_ratio(nutrient_name)
        # If something goes wrong;
        except (
                model.nutrients.exceptions.ChildNutrientExceedsParentMassError
        ) as err:
            # If the value was set previously, and we have a backup, then put it back;
            if backup_nutrient_ratio is not None:
                master_nutrient_ratio.load_data(backup_nutrient_ratio.persistable_data)
            # Otherwise just put it back to its previously unset state;
            else:
                self.undefine_nutrient_ratio(nutrient_name)
            # Pass the exception on;
            raise err

    def zero_nutrient_ratio(self, nutrient_name: str) -> None:
        """Sets the named nutrient ratio to zero."""
        self.set_nutrient_ratio(
            nutrient_name=nutrient_name,
            nutrient_qty=0,
            nutrient_qty_unit='g',
            subject_qty=100,
            subject_qty_unit='g'
        )

    def undefine_nutrient_ratio(self, nutrient_name: str) -> None:
        """Sets the named nutrient ratio to None."""
        self.set_nutrient_ratio(
            nutrient_name=nutrient_name,
            nutrient_qty=None,
            nutrient_qty_unit='g',
            subject_qty=100,
            subject_qty_unit='g'
        )

    def set_nutrient_pref_unit(self, nutrient_name: str, pref_unit: str) -> None:
        """Sets the pref unit for the nutrient ratio."""
        nutrient_ratio = self._get_settable_nutrient_ratio(nutrient_name)
        nutrient_ratio.pref_unit = pref_unit

    def load_data(self, data: Dict[str, Any]) -> None:
        super().load_data(data)
        # Unpack the nutrient ratios data into SettableNutrientRatio instances;
        for nutrient_name, nutrient_ratio_data in data['nutrient_ratios_data'].items():
            # Don't unpack it if it is not defined (to tolerate legacy data);
            if nutrient_ratio_data['nutrient_g_per_subject_g'] is None:
                continue
            # It is defined, go ahead;
            self._nutrient_ratios[nutrient_name] = SettableNutrientRatio(
                nutrient_name=nutrient_name,
                nutrient_ratio_data=nutrient_ratio_data
            )
            self.validate_nutrient_ratio(nutrient_name)

    def persistable_data(self) -> Dict[str, Any]:
        """Returns the nutrient ratio's data in persistable format."""
        data = super().persistable_data
        # Compile the data;
        for nutrient_name, nutrient_ratio in self.nutrient_ratios:
            data['nutrient_ratios_data'][nutrient_name] = nutrient_ratio.persistable_data
        # Return the data;
        return data
