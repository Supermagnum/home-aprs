import logging
import re
from geopy.distance import geodesic
from homeassistant.helpers.entity import Entity
from homeassistant.helpers import discovery
import hamlib

DEFAULT_RADIUS = 50  # Default radius in km
_LOGGER = logging.getLogger(__name__)
FREQUENCY_REGEX = r"(\d{1,3}(?:[.,]\d{3})?)\s*MHz"

def tune_radio(frequency):
    try:
        radio = hamlib.hamlib()
        radio.set_freq(frequency * 1_000_000)
        _LOGGER.info(f"Radio tuned to {frequency} MHz")
    except Exception as e:
        _LOGGER.error(f"Error tuning radio: {e}")

def extract_frequency(aprs_message):
    match = re.search(FREQUENCY_REGEX, aprs_message)
    if match:
        return float(match.group(1).replace(',', '.'))
    return None

def process_aprs_message(aprs_message, user_lat, user_lon, radius_km=DEFAULT_RADIUS):
    frequency = extract_frequency(aprs_message)
    if frequency is None:
        return None
    loc_match = re.search(r"(\-?\d+\.\d+),(\-?\d+\.\d+)", aprs_message)
    if loc_match:
        lat, lon = float(loc_match.group(1)), float(loc_match.group(2))
        if geodesic((lat, lon), (user_lat, user_lon)).km <= radius_km:
            return frequency
    return None

class AprsRadioTunerEntity(Entity):
    def __init__(self, name, aprs_message, user_lat, user_lon, radius_km=DEFAULT_RADIUS):
        self._name = name
        self._aprs_message = aprs_message
        self._user_lat = user_lat
        self._user_lon = user_lon
        self._radius_km = radius_km
        self._frequency = process_aprs_message(aprs_message, user_lat, user_lon, radius_km)

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return f"Frequency: {self._frequency} MHz" if self._frequency else "No Frequency Found"

    def turn_on(self):
        if self._frequency:
            tune_radio(self._frequency)

    def turn_off(self):
        pass
