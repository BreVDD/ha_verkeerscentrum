"""Verkeerscentrum sensor."""
from .__init__ import RSS_SIGN, VerkeersCentrumDateTimeSensor
from .verkeerscentrum_api import VerkeerscentrumAPI
import homeassistant.helpers.config_validation as cv
import logging
import voluptuous as vol

from datetime import timedelta
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_NAME,
)
from .const import *
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator


RSS_SIGN_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_RSS_SIGN_UNIQUE_ID): cv.string,
        vol.Required(CONF_NAME): cv.string,
    }
)

RSS_SIGNS_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_RSS_SIGNS_SIGN): vol.All(cv.ensure_list, [RSS_SIGN_SCHEMA]),
        vol.Required(CONF_RSS_SIGNS_REFRESH_INTERVAL): cv.Number,
    }
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {vol.Required(CONF_RSS_SIGNS): vol.All(RSS_SIGNS_SCHEMA)}
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    async def async_update_data():
        """Fetch data"""

        # Read config
        rssIds = []
        for rss_sign in config[CONF_RSS_SIGNS][CONF_RSS_SIGNS_SIGN]:
            rssIds.append(rss_sign[CONF_RSS_SIGN_UNIQUE_ID])

        api = VerkeerscentrumAPI()
        data = await hass.async_add_executor_job(api.getRSS, rssIds)

        return data

    interval = config[CONF_RSS_SIGNS][CONF_RSS_SIGNS_REFRESH_INTERVAL]

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="verkeerscentrum",
        update_method=async_update_data,
        update_interval=timedelta(seconds=interval),
    )

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_refresh()

    entities_to_add = []
    for rss_sign in config[CONF_RSS_SIGNS][CONF_RSS_SIGNS_SIGN]:
        entities_to_add.append(
            RSS_SIGN(
                coordinator, rss_sign[CONF_RSS_SIGN_UNIQUE_ID], rss_sign[CONF_NAME]
            )
        )

    # Generic settings
    entities_to_add.append(
        VerkeersCentrumDateTimeSensor(
            coordinator,
            "tijd_publicatie",
            "rss_time_publication",
            "RSS Time Publication",
            "mdi:update",
        )
    )

    entities_to_add.append(
        VerkeersCentrumDateTimeSensor(
            coordinator,
            "tijd_laatste_config_wijziging",
            "rss_last_config_change",
            "RSS Last Config Change",
            "mdi:file-clock-outline",
        )
    )

    entities_to_add.append(
        VerkeersCentrumDateTimeSensor(
            coordinator,
            "tijd_laatste_boodschappen_wijziging",
            "rss_last_message_change",
            "RSS Last Message Change",
            "mdi:message-text-clock-outline",
        )
    )

    async_add_entities(entities_to_add)
