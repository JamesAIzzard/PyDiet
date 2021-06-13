"""Defines test fixtures for instructions module."""
from typing import Optional

import model


class HasReadableInstructionSrcTestable(model.instructions.HasReadableInstructionSrc):
    """Minimal implementation to allow testing of HasReadableInstructionSrc."""

    def __init__(self, instruction_src: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)

        self._instruction_src = instruction_src

    @property
    def instruction_src(self) -> str:
        """Returns the instruction source."""
        return self._instruction_src
