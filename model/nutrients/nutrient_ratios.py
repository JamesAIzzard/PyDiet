"""Module defining nutrient ratio functionality."""
import abc
from typing import Dict, List, Any, Optional

import model
import persistence


class NutrientRatioBase(model.quantity.IsQuantityRatioBase, abc.ABC):
    """Extends IsQuantityRatioBase to only allow mass quantities on the subject (nutrient)."""

    def __init__(self, nutrient_name: str, **kwargs):

        # Grab the nutrient instance;
        nutrient_name = model.nutrients.get_nutrient_primary_name(nutrient_name)
        nutrient = model.nutrients.GLOBAL_NUTRIENTS[nutrient_name]

        super().__init__(ratio_subject=nutrient, **kwargs)

    @property
    def nutrient_mass(self) -> 'model.nutrients.ReadonlyNutrientMass':
        """Alias for ratio_subject_qty, specifically returning NutrientMassBase type."""
        return model.nutrients.ReadonlyNutrientMass(
            nutrient_name=self._ratio_subject.primary_name,
            quantity_data_src=lambda: self.quantity_ratio_data['subject_qty_data']
        )

    @property
    def subject_g_per_host_g(self) -> float:
        """Returns the grams of the nutrient per gram of host substance.
        Extends superclass method to covert UndefinedQuantityRatioError into UndefinedNutrientRatioError.
        """
        try:
            return super().subject_g_per_host_g
        except model.quantity.exceptions.UndefinedQuantityRatioError:
            raise model.nutrients.exceptions.UndefinedNutrientRatioError(
                subject=self,
                nutrient_name=self.nutrient_mass.qty_subject.primary_name
            )

    @property
    def subject_qty_in_pref_unit_per_g_of_host(self) -> float:
        """Returns the mass of the nutrient in its pref units, per gram of host substance.
        Extends superclass method to covert UndefinedQuantityRatioError into UndefinedNutrientRatioError.
        """
        try:
            return super().subject_qty_in_pref_unit_per_g_of_host
        except model.quantity.exceptions.UndefinedQuantityRatioError:
            raise model.nutrients.exceptions.UndefinedNutrientRatioError(
                subject=self,
                nutrient_name=self.nutrient_mass.nutrient.primary_name
            )

    @property
    def subject_qty_in_pref_unit_per_ref_qty_of_host(self) -> float:
        """Returns the mass of the nutrient in its preferred unit, which is present in
        the reference quantity/unit of the host substance.
        Extends superclass method to covert UndefinedQuantityRatioError into UndefinedNutrientRatioError.
        """
        try:
            return super().subject_qty_in_pref_unit_per_ref_qty_of_host
        except model.quantity.exceptions.UndefinedQuantityRatioError:
            raise model.nutrients.exceptions.UndefinedNutrientRatioError(
                subject=self,
                nutrient_name=self.nutrient_mass.nutrient.primary_name
            )

    def validate_quantity_ratio(self) -> None:
        """Extends the parent validate nutrient quantity ratio to make exceptions more specific."""
        try:
            super().validate_quantity_ratio()
        except model.quantity.exceptions.SubjectQtyExceedsHostQtyError:
            raise model.nutrients.exceptions.NutrientMassExceedsSubjectQtyError(
                nutrient_mass_value=self.nutrient_mass.ref_qty,
                nutrient_mass_units=self.nutrient_mass.qty_pref_unit,
                host_qty_value=self.ratio_host_qty.ref_qty,
                host_qty_units=self.ratio_host_qty.qty_pref_unit
            )


class ReadonlyNutrientRatio(NutrientRatioBase, model.quantity.IsReadonlyQuantityRatio):
    """Models a readonly nutrient ratio."""


class SettableNutrientRatio(NutrientRatioBase, model.quantity.IsSettableQuantityRatio):
    """Models a settable nutrient ratio."""


class HasReadableNutrientRatios(persistence.YieldsPersistableData, abc.ABC):
    """Abstract class to implement functionality associated with readable nutrient ratios.
    Notes:
        This implementation assumes that only *defined* nutrient ratios are returned by
        the nutrient ratio method. This is useful for various reasons;
        1. We don't store instances which don't contain data.
        2. We don't pass empty fields to the persistence module.
        3. We can use Set mathematics to identify the differences between sets of nutrients, which amount
            to defined and undefined nutrients in certain categories.

        We don't put a store data on this class because not all child classes which have nutrient ratios
        will store/define the data in the same way. For example, the Ingredient class will simply store
        a dictionary of (Settable)ReadableNutrientRatio while a recipe will just store a collection of Ingredient
        instances. Therefore, the way we obtain the nutrient ratios here will depend on the concrete
        implementation of the child class.
    """

    @property
    @abc.abstractmethod
    def nutrient_ratios_data(self) -> 'model.nutrients.NutrientRatiosData':
        """Returns the instance's nutrient ratios data."""
        raise NotImplementedError

    @property
    def defined_nutrient_ratio_names(self) -> List[str]:
        """Returns a list of all of the nutrient names corresponding to nutrient ratios defined
        on the instance."""
        return list(self.nutrient_ratios_data.keys())

    @property
    def nutrient_ratios(self) -> Dict[str, 'ReadonlyNutrientRatio']:
        """Returns a list of nutrient ratios associated with the instance.
        Notes
            These must be readonly instances, to prevent out of context modification without validation.
        """

        # First, create somewhere to store the nutrient ratio instances;
        nrs: Dict[str, 'ReadonlyNutrientRatio'] = {}

        # Next, work the dict and populate the nutrient ratio instances;
        for nutrient_name in self.nutrient_ratios_data.keys():
            nrs[nutrient_name] = self.get_nutrient_ratio(nutrient_name)

        # Now, return the dict of readonly instances;
        return nrs

    def get_nutrient_ratio(self, nutrient_name: str) -> 'ReadonlyNutrientRatio':
        """Returns a ReadableNutrientRatio by name."""

        # Convert to the primary name, in case we were given an alias;
        nutrient_name = model.nutrients.get_nutrient_primary_name(nutrient_name)

        # Cache the nutrient ratios data;
        nrd = self.nutrient_ratios_data

        # If the nutrient is defined (i.e if it is in the dictionary);
        if nutrient_name in nrd.keys():

            # Instantiate and return it;
            return ReadonlyNutrientRatio(
                nutrient_name=nutrient_name,
                ratio_host=self,
                qty_ratio_data_src=lambda: nrd[nutrient_name]
            )

        # Otherwise, return an error to indicate it isn't defined;
        else:
            raise model.nutrients.exceptions.UndefinedNutrientRatioError(
                subject=self,
                nutrient_name=nutrient_name
            )

    @property
    def calories_per_g(self):
        """Returns the number of calories per gram for the instance."""
        # Total the cals/g and return it;
        total_cals_per_g = 0
        for nutrient_name, cals_per_g in model.nutrients.configs.CALORIE_NUTRIENTS.items():
            try:
                total_cals_per_g += self.get_nutrient_ratio(nutrient_name).subject_g_per_host_g * cals_per_g
            except model.nutrients.exceptions.UndefinedNutrientRatioError:
                raise model.nutrients.exceptions.UndefinedCalorieNutrientRatioError(
                    subject=self,
                    nutrient_name=nutrient_name
                )
        return total_cals_per_g

    def nutrient_ratio_is_defined(self, nutrient_name: str) -> bool:
        """Returns True/False to indiciate if the named nutrient ratio has been defined."""
        # Make sure we have the primary nutrient name;
        nutrient_name = model.nutrients.get_nutrient_primary_name(nutrient_name)
        # If it's in the dict, it is defined;
        return nutrient_name in self.nutrient_ratios.keys()

    @property
    def undefined_mandatory_nutrient_ratio_names(self) -> List[str]:
        """Returns a list of the mandatory nutrient ratios which are undefined."""
        return list(set(model.nutrients.configs.MANDATORY_NUTRIENT_NAMES).difference(
            set(self.nutrient_ratios_data.keys())))

    @property
    def defined_optional_nutrient_ratio_names(self) -> List[str]:
        """Returns a list of optional nutrient names which are defined."""
        return list(set(model.nutrients.OPTIONAL_NUTRIENT_NAMES).intersection(set(self.nutrient_ratios_data.keys())))

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
            """Accessor function for the nutrient mass, which raises the correct type of exception."""
            try:
                return self.get_nutrient_ratio(nutr_name).subject_g_per_host_g
            except model.nutrients.exceptions.UndefinedNutrientRatioError:
                raise model.nutrients.exceptions.UndefinedNutrientMassError(
                    subject=self,
                    nutrient_name=nutr_name
                )

        # Call the validator function, passing in our tweaked getter;
        model.nutrients.validation.validate_nutrient_family_masses(
            nutrient_name=nutrient_name,
            get_nutrient_mass_g=get_nutrient_mass_g
        )

    @property
    def persistable_data(self) -> Dict[str, Any]:
        """Returns the nutrient ratio's data in persistable format."""
        data = super().persistable_data

        # Add a heading for the nutrient ratios data;
        data['nutrient_ratios_data'] = self.nutrient_ratios_data

        # Return the data;
        return data


class HasSettableNutrientRatios(HasReadableNutrientRatios, persistence.CanLoadData):
    """Class to implement functionality associated with settable nutrient ratios.
    Notes:
        To make sure any changes to ReadableNutrientRatio instances pass through the family validation
        process, its important not to give out SettableNutrientRatio instances. All changes to nutrient
        ratios must be implemented through this class' methods.

        All classes which have SettableNutrientRatios also store them locally, so we can add a
        constructor here, with a local dictionary to store the data. Also, since we now know the
        instance is storing data locally, we can also inherit from HasPersistableData, and provide
        concrete implementations of its methods to get data into and out of the instance.
    """

    def __init__(self, nutrient_ratios_data: Optional[Dict[str, 'model.quantity.QuantityRatioData']] = None, **kwargs):
        super().__init__(**kwargs)

        # Now we are storing the data locally, so create somewhere to store it.
        # Since nutrient ratios are complex classes, we initialise them, instead of just storing
        # persistable data. This means we don't have to re-initailise them every time_str we want to do
        # utilise functionality from the ReadableNutrientRatio class.
        self._nutrient_ratios: Dict[str, 'SettableNutrientRatio'] = {}

        # If we got data, then load it up;
        if nutrient_ratios_data is not None:
            self.load_data({'nutrient_ratios_data': nutrient_ratios_data})

    @property
    def nutrient_ratios_data(self) -> 'model.nutrients.NutrientRatiosData':
        """Returns the instance's current nutrient ratios data."""
        # Init the dict;
        data: 'model.nutrients.NutrientRatiosData' = {}

        # Compile the data;
        for nutrient_name, nutrient_ratio in self._nutrient_ratios.items():
            data[nutrient_name] = nutrient_ratio.persistable_data

        # Return;
        return data

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
                           nutrient_mass_value: Optional[float],
                           nutrient_mass_unit: str,
                           host_qty_value: Optional[float],
                           host_qty_unit: str) -> None:
        """Sets the data on the named nutrient ratio, and runs family validation."""

        # Make sure we are dealing with the nutrient's primary name;
        nutrient_name = model.nutrients.get_nutrient_primary_name(nutrient_name)

        # We can't break anything if we are unsetting the nutrient, so just go ahead and do it and skip the rest;
        if nutrient_mass_value is None:
            nr = self._get_settable_nutrient_ratio(nutrient_name)
            nr.unset_quantity_ratio()

        # Grab the settable nutrient ratio instance;
        try:
            master_nutrient_ratio = self._get_settable_nutrient_ratio(nutrient_name)
        except model.nutrients.exceptions.UndefinedNutrientRatioError:
            # OK, we don't have this one yet. Create it;
            self._nutrient_ratios[nutrient_name] = SettableNutrientRatio(
                nutrient_name=nutrient_name,
                ratio_host=self,
                qty_ratio_data=model.quantity.QuantityRatioData(
                    subject_qty_data=model.quantity.QuantityData(
                        quantity_in_g=None,
                        pref_unit='g'
                    ),
                    host_qty_data=model.quantity.QuantityData(
                        quantity_in_g=None,
                        pref_unit='g'
                    )
                )
            )
            master_nutrient_ratio = self._get_settable_nutrient_ratio(nutrient_name)

        # Take a backup of the data;
        backup_data = master_nutrient_ratio.persistable_data

        # Now ahead and make the change;
        master_nutrient_ratio.set_quantity_ratio(
            subject_quantity_value=nutrient_mass_value,
            subject_quantity_unit=nutrient_mass_unit,
            host_quantity_value=host_qty_value,
            host_quantity_unit=host_qty_unit
        )

        # Final step is to run the validation;
        try:
            self.validate_nutrient_ratio(nutrient_name)
        # If something goes wrong;
        except (
                model.nutrients.exceptions.ChildNutrientExceedsParentMassError
        ) as err:
            master_nutrient_ratio.load_data(backup_data)
            # Pass the exception on;
            raise err

    def undefine_nutrient_ratio(self, nutrient_name: str) -> None:
        """Sets the named nutrient ratio to None."""
        # Make sure we have the primary version of the nutrient name;
        nutrient_name = model.nutrients.get_nutrient_primary_name(nutrient_name)
        # If we have it, delete it;
        if self.nutrient_ratio_is_defined(nutrient_name):
            del self._nutrient_ratios[nutrient_name]

    def zero_nutrient_ratio(self, nutrient_name: str) -> None:
        """Sets the named nutrient ratio to zero."""
        self.set_nutrient_ratio(
            nutrient_name=nutrient_name,
            nutrient_mass_value=0,
            nutrient_mass_unit='g',
            host_qty_value=100,
            host_qty_unit='g'
        )

    def load_data(self, data: Dict[str, Any]) -> None:
        """Loads the instance data."""
        super().load_data(data)

        # If we don't have any fields in this data, exit;
        if 'nutrient_ratios_data' not in data.keys():
            return

        # Unpack the nutrient ratios data into SettableNutrientRatio instances;
        for nutrient_name, quantity_ratio_data in data['nutrient_ratios_data'].items():

            # Don't unpack it if it is not defined (to tolerate legacy data);
            if model.quantity.quantity_ratio_data_is_defined(quantity_ratio_data) is False:
                continue

            # It is defined, go ahead;
            self._nutrient_ratios[nutrient_name] = SettableNutrientRatio(
                ratio_host=self,
                nutrient_name=nutrient_name,
                qty_ratio_data=quantity_ratio_data,
            )

            # Run validation now this nr has been added;
            self.validate_nutrient_ratio(nutrient_name)
