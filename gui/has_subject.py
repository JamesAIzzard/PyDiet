from typing import Any


class HasSubject:
    """Defines the API for any controller with a subject."""

    def __init__(self, subject_type: Any, **kwargs):
        self._subject_type = subject_type
        self._subject: Any = None

    @property
    def subject(self) -> Any:
        """Returns the subject."""
        return self._subject

    @subject.setter
    def subject(self, subject: Any) -> None:
        """Sets the subject."""
        if not isinstance(subject, self._subject_type):
            raise TypeError(f"Subject must be an instance of {self._subject_type}")
        self._subject = subject
