import logging
import requests
import voluptuous as vol
from datetime import timedelta
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE, CONF_RADIUS
from .config_flow import CONF_API_KEY

DOMAIN = "aprs_radio_tuner"
_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=1)
FREQUENCY_REGEX = r"(\d{3}[.,]\d{1,3})\s*MHz"

def extract_frequency(aprs_message):
    if "qrv" not in aprs_message.lower():
        return None
    import re
    match = re.search(FREQUENCY_REGEX, aprs_message)
    if match:
        return float(match.group(1).replace(',', '.'))
    return None

async def async_setup(hass, config):
    return True

async def async_setup_entry(hass, entry):
    lat = entry.data[CONF_LATITUDE]
    lon = entry.data[CONF_LONGITUDE]
    radius_km = entry.data[CONF_RADIUS]
    api_key = entry.data[CONF_API_KEY]

    async def poll_aprsfi(now):
        try:
            bbox = f"{lon - 0.1},{lat - 0.1},{lon + 0.1},{lat + 0.1}"
            url = f"https://api.aprs.fi/api/get?bbox={bbox}&what=loc&apikey={api_key}&format=json"
            response = requests.get(url, timeout=10)
            data = response.json()

            if "entries" in data:
                for station in data["entries"]:
                    comment = station.get("comment", "")
                    freq = extract_frequency(comment)
                    if freq:
                        _LOGGER.info(f"Tuning radio to {freq} MHz from {station['name']}")
                        requests.post("http://localhost:5000/radio/tune", json={"frequency": freq})
                        hass.components.persistent_notification.create(
                            f"{station['name']} is QRV on {freq} MHz", title="APRS QRV Alert"
                        )
        except Exception as e:
            _LOGGER.error(f"Error polling aprs.fi: {e}")

    async_track_time_interval(hass, poll_aprsfi, SCAN_INTERVAL)
    return True
