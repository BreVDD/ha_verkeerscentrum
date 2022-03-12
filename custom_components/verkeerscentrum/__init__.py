"""The verkeerscentrum integration."""
from __future__ import annotations
from homeassistant.core import Config, HomeAssistant
from homeassistant.helpers.typing import ConfigType


async def async_setup(hass: HomeAssistant, config: Config) -> bool:
    """Set up the Verkeerscentrum component."""
    return True
