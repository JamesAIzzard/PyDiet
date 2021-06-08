"""Defines recipe classes."""

import abc
from typing import Dict, List, Optional

import model
import persistence


class RecipeBase(
    model.HasReadableName,
    abc.ABC
):
    """Abstract base class for readable and writbale recipe classes."""
