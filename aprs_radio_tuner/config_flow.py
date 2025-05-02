import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE, CONF_RADIUS
import logging

_LOGGER = logging.getLogger(__name__)

class AprsRadioTunerConfigFlow(config_entries.ConfigFlow, domain="aprs_radio_tuner"):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="APRS Radio Tuner", data=user_input)
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_LATITUDE): float,
                vol.Required(CONF_LONGITUDE): float,
                vol.Optional(CONF_RADIUS, default=50): int,
            }),
        )
