"""Coordinator for radiotherm."""
from __future__ import annotations

from datetime import timedelta
import logging
from socket import timeout

from radiotherm.validate import RadiothermTstatError

from homeassistant.core import HomeAssistant
from homeassistant.helpers.debounce import Debouncer
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .data import RadioThermInitData, RadioThermUpdate, async_get_data

_LOGGER = logging.getLogger(__name__)

UPDATE_INTERVAL = timedelta(seconds=15)

REQUEST_REFRESH_DELAY = 3


class RadioThermUpdateCoordinator(DataUpdateCoordinator[RadioThermUpdate]):
    """DataUpdateCoordinator to gather data for radio thermostats."""

    def __init__(
        self,
        hass: HomeAssistant,
        host: str,
        init_data: RadioThermInitData,
    ) -> None:
        """Initialize DataUpdateCoordinator."""
        self.device = init_data.tstat
        self.host = host
        self.name = init_data.name
        super().__init__(
            hass,
            _LOGGER,
            name=f"radiotherm {self.name}",
            update_interval=UPDATE_INTERVAL,
            # We don't want an immediate refresh since the device
            # takes a moment to reflect the state change
            request_refresh_debouncer=Debouncer(
                hass, _LOGGER, cooldown=REQUEST_REFRESH_DELAY, immediate=False
            ),
        )

    async def _async_update_data(self) -> RadioThermUpdate:
        """Update data from the thermostat."""
        try:
            return await async_get_data(self.hass, self.device)
        except RadiothermTstatError as ex:
            raise UpdateFailed(
                f"{self.name} ({self.host}) was busy (invalid value returned): {ex}"
            ) from ex
        except timeout as ex:
            raise UpdateFailed(
                f"{self.name} ({self.host}) timed out waiting for a response: {ex}"
            ) from ex
