"""Verkeerscentrum sensor."""
from .classes import (
    RSS_SIGN,
    VerkeersCentrumDateTimeSensor,
)
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
        vol.Required(CONF_RSS_SIGN_SITE_NAME): cv.string,
        vol.Required(CONF_NAME): cv.string,
    }
)

RSS_INDIVIDUAL_SIGN_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_RSS_SIGN_UNIQUE_ID): cv.string,
        vol.Required(CONF_NAME): cv.string,
    }
)

RSS_SIGNS_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_RSS_SIGNS_SIGN): vol.All(cv.ensure_list, [RSS_SIGN_SCHEMA]),
        vol.Optional(CONF_RSS_SIGNS_INDIVIDUAL_SIGN): vol.All(
            cv.ensure_list, [RSS_INDIVIDUAL_SIGN_SCHEMA]
        ),
        vol.Optional(CONF_RSS_SIGNS_REFRESH_INTERVAL, default=3 * 60): cv.Number,
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
        if CONF_RSS_SIGNS_INDIVIDUAL_SIGN in config[CONF_RSS_SIGNS]:
            for rss_sign in config[CONF_RSS_SIGNS][CONF_RSS_SIGNS_INDIVIDUAL_SIGN]:
                rssIds.append(rss_sign[CONF_RSS_SIGN_UNIQUE_ID])

        rssSiteNames = []
        if CONF_RSS_SIGNS_SIGN in config[CONF_RSS_SIGNS]:
            for rss_sign in config[CONF_RSS_SIGNS][CONF_RSS_SIGNS_SIGN]:
                rssSiteNames.append("/{}/".format(rss_sign[CONF_RSS_SIGN_SITE_NAME]))

        api = VerkeerscentrumAPI()
        data = await hass.async_add_executor_job(api.getRSS, rssIds, rssSiteNames)

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
    if CONF_RSS_SIGNS_INDIVIDUAL_SIGN in config[CONF_RSS_SIGNS]:
        for rss_sign in config[CONF_RSS_SIGNS][CONF_RSS_SIGNS_INDIVIDUAL_SIGN]:
            entities_to_add.append(
                RSS_SIGN(
                    coordinator, rss_sign[CONF_RSS_SIGN_UNIQUE_ID], rss_sign[CONF_NAME]
                )
            )

    site_names_and_name = {}
    for rss_sign in config[CONF_RSS_SIGNS][CONF_RSS_SIGNS_SIGN]:
        site_names_and_name[
            "/{}/".format(rss_sign[CONF_RSS_SIGN_SITE_NAME])
        ] = rss_sign[CONF_NAME]

    for rss_sign in coordinator.data.rss_borden:
        for site_name in site_names_and_name.keys():
            if site_name in rss_sign.abbameldanaam:
                unique_ha_name = site_names_and_name[site_name]

                # Find out the number of the sign
                unique_ha_name = (
                    unique_ha_name
                    + " - "
                    + rss_sign.abbameldanaam.split("/")[-1]
                    .replace("VOORBORD", "Pre-sign ")
                    .replace("ACHTERBORD", "After-sign ")
                    .replace("BORD", "Sign ")
                )

                entities_to_add.append(
                    RSS_SIGN(coordinator, rss_sign.unieke_id, unique_ha_name)
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
