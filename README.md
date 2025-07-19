
# E-Ink Digital Clock & Weather Display

A Python-based digital and analog clock with weather forecast for Waveshare 7.5-inch e-ink displays, designed for Raspberry Pi.

## Overview

This project creates a dual-format clock display that shows both digital and analog time, plus a 3-day weather forecast, on an e-ink screen. The display updates every minute and is perfect for a low-power, always-on desktop clock or weather station.

## Features

- **Digital Clock**: Clear time display in HH:MM format, positioned below the analog clock
- **Analog Clock**: Traditional clock face with selectable hour marks (numbers or lines)
- **Weather Forecast**: 3-day, 3-times-per-day forecast (morning, noon, evening) from OpenWeatherMap
- **German Weekday Support**: Weekday names shown in German if locale is available
- **Configurable via .env**: API key, location, and clock mark style set in `.env` file
- **Low Power**: Optimized for e-ink displays with minimal power consumption
- **Auto-refresh**: Updates every 60 seconds

## Hardware Requirements

- Raspberry Pi (any model with GPIO pins)
- Waveshare 7.5-inch e-ink display (V2)
- Proper connections between Raspberry Pi and e-ink display

## Software Dependencies

- Python 3.x
- Waveshare e-ink display library (`waveshare_epd`)
- PIL (Python Imaging Library) / Pillow
- python-dotenv
- requests
- Standard Python libraries: `math`, `time`, `datetime`, `os`, `locale`

## Installation

1. Install the required Python packages:
   ```bash
   pip install Pillow python-dotenv requests
   ```

2. Install the Waveshare e-ink display library following their official documentation

3. Ensure the DejaVu Sans font is available:
   ```bash
   sudo apt-get install fonts-dejavu-core
   ```

4. (Optional) Enable German locale for German weekday names:
   ```bash
   sudo dpkg-reconfigure locales
   # Select de_DE.UTF-8 and generate
   ```

## Usage

1. Copy `.env.example` to `.env` and fill in your OpenWeatherMap API key and location:
   ```
   API_KEY=your_openweathermap_api_key
   LAT=50.2577
   LON=10.9660
   CLOCK_MARKS=numbers  # or 'lines'
   ```

2. Run the script directly:
   ```bash
   python waveshare75_raspbi.py
   ```

The display will show:
- **Left**: 3-day weather forecast (morning, noon, evening) with German weekday names if locale is set
- **Right**: Analog clock face (numbers or lines, configurable)
- **Below analog clock**: Digital time display, centered and sized appropriately

## Display Layout

- **Screen Resolution**: 800×480 pixels
- **Analog Clock Center**: (600, 160)
- **Clock Radius**: 130 pixels
- **Digital Clock**: Centered below analog clock with 54px font
- **Weather Forecast**: Left half, 3 days, 3 times per day
## Configuration

All configuration is done via the `.env` file:

- `API_KEY`: Your OpenWeatherMap API key
- `LAT`, `LON`: Latitude and longitude for weather location
- `CLOCK_MARKS`: `numbers` for hour numbers, `lines` for tick marks

Example:
```
API_KEY=your_openweathermap_api_key
LAT=50.2577
LON=10.9660
CLOCK_MARKS=lines
```
- **Clock Face Numbers**: 24px font at 12, 3, 6, 9 positions
- **Hour Marks**: Lines at remaining hour positions
- **Background**: White
- **Text/Graphics**: Black

## Code Structure

- **Initialization**: Sets up the e-ink display and loads fonts (digital and number fonts)
- **Main Loop**: Continuously updates the display every minute
- **Time Calculation**: Converts current time to both digital and analog formats
- **Clock Face Drawing**: Creates numbered hours and hour mark lines
- **Hand Drawing**: Renders hour and minute hands with proper positioning
- **Digital Display**: Centers digital time below the analog clock

## Customization

You can easily modify:
- Clock positions by changing `center_x`, `center_y` coordinates
- Clock size by adjusting the `radius` value
- Font sizes by modifying the `font_digital` and `font_numbers` parameters
- Digital clock positioning relative to analog clock
- Hour marking styles (numbers vs. lines)
- Update frequency by changing the `time.sleep(60)` value

## Notes

- The analog clock uses 12-hour format with traditional numbered face
- Hour hand length is 60% of the minute hand for traditional appearance
- Numbers appear at 12, 3, 6, and 9 o'clock positions
- Hour marks are shown as lines for positions 1, 2, 4, 5, 7, 8, 10, 11
- Digital time is automatically centered below the analog clock
- The display is optimized for the monochrome e-ink format
- Updates are intentionally limited to once per minute to preserve display lifespan
