from typing import Any


class HasSubject:
    """Defines the API for any controller with a subject."""

    def __init__(self, subject_type: Any, **kwargs):
        self.subject_type = subject_type
        self._subject: Any = None

    def _set_subject(self, subject: Any) -> None:
        """Method to set subject to allow overriding/extending in child class."""
        if not isinstance(subject, self.subject_type):
            raise TypeError(f"Subject must be an instance of {self.subject_type}")
        self._subject = subject

    @property
    def subject(self) -> Any:
        """Returns the subject."""
        return self._subject

    @subject.setter
    def subject(self, subject: Any) -> None:
        """Sets the subject."""
        self._set_subject(subject)
