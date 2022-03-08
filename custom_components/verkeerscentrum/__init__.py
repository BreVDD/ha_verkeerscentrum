"""The verkeerscentrum integration."""
from __future__ import annotations
from homeassistant.const import DEVICE_CLASS_TIMESTAMP
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.core import Config, HomeAssistant
from homeassistant.helpers.typing import ConfigType
from datetime import datetime
from homeassistant.components.sensor import SensorEntity


async def async_setup(hass: HomeAssistant, config: Config) -> bool:
    """Set up the Verkeerscentrum component."""
    return True


class VerkeersCentrumSensor(CoordinatorEntity, SensorEntity):
    """Verkeers Centrum Sensor Class"""

    def __init__(self, coordinator, unique_id, name, icon):
        """Initialize the entity"""
        super().__init__(coordinator)
        self._unique_id = unique_id
        self._name = name
        if icon is not None:
            self._attr_icon = icon

    @property
    def name(self) -> str:
        return self._name

    @property
    def native_value(self) -> str:
        return self.state if self.state else ""

    @property
    def unique_id(self) -> str:
        return self._unique_id


class RSS_SIGN(VerkeersCentrumSensor):
    """RSS SIGN Class"""

    def __init__(self, coordinator, unique_id, name):
        """Initialize the entity"""
        save_unique_id = unique_id.replace(";", "_").replace("RSS_", "")
        super().__init__(coordinator, f"rss_sign_{save_unique_id}", name, None)
        self._id = unique_id

    @property
    def icon(self) -> str | None:
        state = self.state

        if state == "GROENE_PIJL":
            return "mdi:arrow-down-bold"
        if state == "PIJL_LINKS":
            return "mdi:arrow-bottom-left-thick"
        if state == "PIJL_RECHTS":
            return "mdi:arrow-bottom-right-thick"
        if state == "KRUIS":
            return "mdi:close-thick"
        if "SNELH" in state:
            return "mdi:car-speed-limiter"
        if state == "UITROEP_NU":
            return "mdi:alert-outline"
        if state == "FILE":
            return "mdi:car-emergency"
        else:
            return "mdi:road-variant"

    @property
    def state(self) -> str:
        if self.coordinator.data:
            for rss_sign in self.coordinator.data.rss_borden:
                if rss_sign.unieke_id == self._id:
                    return rss_sign.verkeersteken_status
        return None

    @property
    def state_attributes(self):
        if self.coordinator.data:
            for rss_sign in self.coordinator.data.rss_borden:
                if rss_sign.unieke_id == self._id:
                    return {
                        "defect": rss_sign.defect,
                        "active": rss_sign.inDienst,
                        "flashing": rss_sign.knipperlicht_status,
                        "arrow": rss_sign.pijl_status,
                        "bottom_plate": rss_sign.onderbord_status,
                        "sign": rss_sign.verkeersteken_status,
                        "last_updated": rss_sign.laatst_gewijzigd,
                    }
        return None


class VerkeersCentrumDateTimeSensor(VerkeersCentrumSensor):
    """RSS SIGN Class"""

    def __init__(self, coordinator, date_property, unique_id, name, icon):
        """Initialize the entity"""
        super().__init__(coordinator, unique_id, name, icon)
        self._date_property = date_property
        self._attr_device_class = DEVICE_CLASS_TIMESTAMP

    @property
    def state(self) -> str:
        data = getattr(self.coordinator.data, self._date_property)
        if self.coordinator.data:
            if data:
                return datetime.fromisoformat(data)
        return None
