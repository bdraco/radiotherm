"""The radiotherm component models."""
from __future__ import annotations

from dataclasses import dataclass

from .coordinator import RadioThermUpdateCoordinator
from .data import RadioThermInitData


@dataclass
class RadioThermData:
    """Data for the radiothem integration."""

    coordinator: RadioThermUpdateCoordinator
    init_data: RadioThermInitData
    hold_temp: bool
