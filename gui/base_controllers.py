import abc
import tkinter as tk
from typing import List, Callable, Any


class BaseController:
    """Base class for view controllers."""

    def __init__(self, view: 'tk.Widget', **kwargs):
        super().__init__(**kwargs)
        self._children: List['BaseController'] = []
        self._view = view

    @property
    @abc.abstractmethod
    def view(self) -> 'Any':
        """Returns the view associated with the controller instance."""
        return self._view

    @abc.abstractmethod
    def update_view(self, *args, **kwargs) -> None:
        """Push data from the model to the view."""
        raise NotImplementedError

    @abc.abstractmethod
    def process_view_changes(self, *args, **kwargs) -> None:
        """Push data from the view to the model."""
        raise NotImplementedError


class AppPage(BaseController, abc.ABC):
    """Base class for controllers that the app can handle as main pages."""

    def __init__(self, title: str, on_page_load: Callable[..., None], on_page_close: Callable[..., None], **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.on_page_load = on_page_load
        self.on_page_close = on_page_close



class HasSubject(BaseController, abc.ABC):
    """Base class for view controllers with subject."""

    def __init__(self, subject_type: Any, **kwargs):
        super().__init__(**kwargs)
        self._subject_type = subject_type
        self._subject: Any = None

    @property
    @abc.abstractmethod
    def subject(self) -> Any:
        """Returns the subject."""
        return self._subject

    @abc.abstractmethod
    def set_subject(self, subject: Any) -> None:
        """Method to set subject to allow overriding/extending in child class."""
        # Check the subject is the right type;
        if not isinstance(subject, self._subject_type):
            raise TypeError(f"Subject must be an instance of {self._subject_type}")
        # Assign it;
        self._subject = subject
        # Update the view to reflect it;
        self.update_view()


class SupportsValidity(abc.ABC):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    @abc.abstractmethod
    def is_valid(self) -> bool:
        """Returns True/False to indicate if the element is valid."""
        raise NotImplementedError

    @property
    def is_invalid(self) -> bool:
        """Returns True/False to indicate if the element is invalid."""
        return not self.is_valid


class SupportsDefinition(abc.ABC):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    @abc.abstractmethod
    def is_defined(self) -> bool:
        """Returns True/False to indicate if the element is defined."""
        raise NotImplementedError

    @property
    def is_undefined(self) -> bool:
        """Returns True/False to indicate if the element is undefined."""
        return not self.is_defined
