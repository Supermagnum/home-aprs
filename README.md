# home-aprs
# APRS Radio Tuner for Home Assistant

This custom integration monitors APRS messages and automatically tunes your Ham radio (via [Hamlib](https://hamlib.github.io/)) to any QRV frequency announced by a station within a configurable radius of your location.

## Features

- Monitors APRS.FI messages for QRV frequencies (e.g., `145.500MHz`, `145,500MHz`)
- Parses frequency and geographic coordinates from APRS messages
- Checks if the station is within a user-defined radius
- Tunes a Hamlib-compatible radio to the extracted frequency
- Optional UI to configure latitude, longitude, and radius
- Notifies user when a valid APRS station is detected

## Installation

1. **Download and extract the integration:**


2. **Place the contents** in your Home Assistant configuration folder:
   ```
   <config_dir>/custom_components/aprs_radio_tuner/
   ```

3. **Install required dependencies:**
   ```bash
   pip install pyaprs pyhamlib geopy
   ```

4. **Restart Home Assistant.**

## Configuration

### UI Configuration

Navigate to:

**Settings → Devices & Services → Integrations → + Add Integration → APRS Radio Tuner**

You'll be prompted to enter:

- **Latitude:** Your home’s latitude
- **Longitude:** Your home’s longitude
- **Radius:** Detection area in kilometers (default: 50 km)
- ** Your APRS.FI api key.

### Example YAML (Advanced / Manual Setup)

```yaml
aprs_radio_tuner:
  latitude: 59.9111
  longitude: 10.7528
  radius: 30
```

## How It Works

1. APRS messages are parsed to extract geographic coordinates and QRV frequencies.
2. If a station is within the configured radius, the frequency is passed to Hamlib.
3. The Hamlib API is used to tune your connected radio to that frequency.

**Supported formats:**
- `145.500 MHz`
- `145,500 MHz`

## Requirements

- A Hamlib-compatible transceiver connected to your system.
- APRS feed (e.g., via pyaprs or your own parser).
- Home Assistant with custom component support enabled.

## Troubleshooting

- Make sure Hamlib is installed and your radio is properly configured.
- Check Home Assistant logs for errors (`Configuration → Logs`).
- Ensure dependencies are installed in the same environment as Home Assistant.

## Future Ideas

- Optional speech announcement or TTS notification
- Track which stations repeat QRV alerts
- Integrate with maps to visualize QRV coverage

## WARNING: this addon is untested! 
