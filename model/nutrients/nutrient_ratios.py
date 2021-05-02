import abc
from typing import Dict, List, Any, Optional, TypedDict

import model
import persistence


class NutrientRatioData(TypedDict):
    """Persisted data format for NutrientRatio instances."""
    nutrient_qty_data: model.quantity.QuantityData
    subject_ref_qty_data: model.quantity.QuantityData


NutrientRatiosData = Dict[str, 'NutrientRatioData']


class NutrientRatio(model.SupportsDefinition, persistence.CanLoadData):
    """Models an amount of nutrient per substance."""

    def __init__(self, nutrient_name: str,
                 subject: Any,
                 nutrient_ratio_data: Optional['NutrientRatioData'] = None,
                 **kwargs):
        super().__init__(**kwargs)

        # Make sure we are using the primary name;
        nutrient_name = model.nutrients.get_nutrient_primary_name(nutrient_name)

        self._nutrient_mass = model.nutrients.NutrientMass(
            nutrient_name=nutrient_name,
            mass_data=model.quantity.QuantityData(
                quantity_in_g=None,
                ref_qty=100,
                pref_unit='g'
            )
        )
        self._subject_ref_qty = model.quantity.QuantityOf(
            subject=subject,
            quantity_data=model.quantity.QuantityData(
                quantity_in_g=None,
                ref_qty=100,
                pref_unit='g'
            )
        )

        # If data was provided, go ahead and load it;
        if nutrient_ratio_data is not None:
            self.load_data(nutrient_ratio_data)

    @property
    def nutrient_mass(self) -> 'model.nutrients.NutrientMass':
        """Returns the nutrient associated with the nutrient ratio."""
        return self._nutrient_mass

    @property
    def nutrient_name(self) -> str:
        """Shortcut property to pull out the nutrient name."""
        return self.nutrient_mass.nutrient.primary_name

    @property
    def subject_quantity(self) -> 'model.quantity.QuantityOf':
        """Returns the subject quantity associated with the nutrient ratio."""
        return self._subject_ref_qty

    @property
    def g_per_subject_g(self) -> Optional[float]:
        """Returns the grams of the nutrient per gram of subject."""

        # Catch an undefined nutrient mass first off;
        if not self._nutrient_mass.is_defined:
            raise model.nutrients.exceptions.UndefinedNutrientRatioError(
                subject=self._subject_ref_qty.subject,
                nutrient_name=self.nutrient_name
            )

        # OK, calc and return;
        return self._nutrient_mass.quantity_in_g / self._subject_ref_qty.quantity_in_g

    @property
    def mass_in_nutrient_pref_unit_per_subject_g(self) -> float:
        """Returns the mass of the nutrient in its pref units, per gram of subject."""
        return model.quantity.convert_qty_unit(
            qty=self.g_per_subject_g,
            start_unit='g',
            end_unit=self.nutrient_mass.pref_unit
        )

    @property
    def mass_in_nutrient_pref_unit_per_subject_ref_qty(self) -> float:
        """Returns the mass of the nutrient in its preferred unit, which is present in
        the reference quantity/unit of the subject."""
        return self.mass_in_nutrient_pref_unit_per_subject_g * self.subject_quantity.quantity_in_g

    @property
    def is_defined(self) -> bool:
        """Returns True/False to indicate if the nutrient ratio is fully defined."""
        return self.nutrient_mass.is_defined

    @property
    def is_zero(self) -> bool:
        """Returns True/False to indicate if the nutrient ratio is explicitly set to zero."""
        return self.g_per_subject_g == 0

    @property
    def is_non_zero(self) -> bool:
        """Returns True/False to indicate if the nutrient ratio is not zero."""
        return not self.is_zero

    def load_data(self, nutrient_ratio_data: 'NutrientRatioData') -> None:
        self.nutrient_mass.load_data(nutrient_ratio_data['nutrient_qty_data'])
        self._subject_ref_qty.load_data(nutrient_ratio_data['subject_ref_qty_data'])

    @property
    def persistable_data(self) -> Dict[str, Any]:
        return model.nutrients.NutrientRatioData(
            nutrient_qty_data=self.nutrient_mass.persistable_data,
            subject_ref_qty_data=self._subject_ref_qty.persistable_data
        )


class SettableNutrientRatio(NutrientRatio):
    """Models a settable nutrient ratio. Careful where you return these! Nutrient ratios
    shouldn't be set without mutually validating all nutrients on the subject.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Check that we don't have readonly flag_data (this would allow inconsistencies);
        if not isinstance(self, model.flags.HasSettableFlags):
            assert not isinstance(self, model.flags.HasFlags)

        # Convert the nutrient mass and subject ref qty to settable versions;
        self._nutrient_mass = model.nutrients.SettableNutrientMass(
            nutrient_name=self._nutrient_mass.nutrient.primary_name,
            mass_data=self._nutrient_mass.persistable_data
        )
        self._subject_ref_qty = model.quantity.SettableQuantityOf(
            subject=self._subject_ref_qty.subject,
            quantity_data=self._subject_ref_qty.persistable_data
        )

    def set_ratio(self, nutrient_mass: Optional[float],
                  nutrient_mass_unit: str,
                  subject_qty: Optional[float],
                  subject_qty_unit: str
                  ) -> None:
        """Sets the nutrient ratio in arbitrary units."""
        # Take a backup in case we get an exception during setting;
        backup_data = self.persistable_data
        try:
            self._nutrient_mass.set_quantity(
                quantity=nutrient_mass,
                unit=nutrient_mass_unit
            )
            self._subject_ref_qty.set_quantity(
                quantity=subject_qty,
                unit=subject_qty_unit
            )
        except model.quantity.exceptions.BaseQuantityError as err:
            self.load_data(backup_data)
            raise err

        # Check the nutrient qty doesn't exceed the subject qty;
        if self._nutrient_mass.quantity_in_g > self._subject_ref_qty.quantity_in_g:
            self.load_data(backup_data)
            raise model.nutrients.exceptions.NutrientQtyExceedsSubjectQtyError(
                subject=self,
                nutrient_name=self.nutrient_name,
                nutrient_mass=nutrient_mass,
                nutrient_mass_units=nutrient_mass_unit,
                subject_qty=subject_qty,
                subject_qty_units=subject_qty_unit
            )

    def undefine(self) -> None:
        """Resets g_per_subject_g to None and pref_unit to 'g'."""
        self.set_ratio(
            nutrient_mass=None,
            nutrient_mass_unit='g',
            subject_qty=None,
            subject_qty_unit='g'
        )

    def zero(self) -> None:
        """Zeroes the nutrient ratio."""
        self.set_ratio(
            nutrient_mass=0,
            nutrient_mass_unit=self.nutrient_mass.pref_unit,
            subject_qty=self._subject_ref_qty.ref_qty,
            subject_qty_unit=self._subject_ref_qty.pref_unit
        )


class HasNutrientRatios(abc.ABC):
    """Abstract class to model objects with readonly nutrient ratios.
    Notes:
        This implementation assumes that only *defined* nutrient ratios are returned by
        the nutrient ratio method. This is useful for various reasons;
        1. We don't store instances which don't contain data.
        2. We don't pass empty fields to the persistence module.
        3. We can use Set mathematics to identify the differences between sets of nutrients, which amount
            to defined and undefined nutrients in certain categories.

        We don't put a store data on this class because not all child classes which have nutrient ratios
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
        nutrient_ratio = self.get_nutrient_ratio(nutrient_name)
        return nutrient_ratio.mass_in_nutrient_pref_unit_per_subject_ref_qty

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


class HasSettableNutrientRatios(HasNutrientRatios, persistence.CanLoadData):
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
                subject=self,
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
                           nutrient_mass: Optional[float],
                           nutrient_mass_unit: str,
                           subject_qty: float,
                           subject_qty_unit: str) -> None:
        """Sets the data on the named nutrient ratio, and runs family validation."""

        # Catch zero subject quantity;
        if subject_qty == 0:
            raise model.quantity.exceptions.ZeroQtyError(subject=self)

        # Make sure we are dealing with the nutrient's primary name;
        nutrient_name = model.nutrients.get_nutrient_primary_name(nutrient_name)

        # We can't break anything if we are unsetting the nutrient, so just go ahead and do it and skip the rest;
        if nutrient_mass is None:
            self.undefine_nutrient_ratio(nutrient_name)

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

        # Now ahead and make the change;
        master_nutrient_ratio.set_ratio(
            nutrient_mass=nutrient_mass,
            nutrient_mass_unit=nutrient_mass_unit,
            subject_qty=subject_qty,
            subject_qty_unit=subject_qty_unit
        )

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

    def undefine_nutrient_ratio(self, nutrient_name: str) -> None:
        """Sets the named nutrient ratio to None."""
        # Make sure we have the primary version of the nutrient name;
        nutrient_name = model.nutrients.get_nutrient_primary_name(nutrient_name)
        # If we have it, delete it;
        if self.nutrient_ratio_is_defined(nutrient_name):
            del self._nutrient_ratios[nutrient_name]

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
