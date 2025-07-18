# E-Ink Digital Clock Display

A Python-based digital clock application for Waveshare 7.5-inch e-ink displays, designed to run on Raspberry Pi.

## Overview

This project creates a dual-format clock display that shows both digital and analog time on an e-ink screen. The display updates every minute and is perfect for a low-power, always-on desktop clock.

## Features

- **Digital Clock**: Clear time display in HH:MM format, positioned below the analog clock
- **Analog Clock**: Traditional clock face with numbered hours (12, 3, 6, 9) and hour mark lines
- **Professional Design**: Properly centered layout with clock face numbers and hour markings
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
- Standard Python libraries: `math`, `time`, `datetime`, `os`

## Installation

1. Install the required Python packages:
   ```bash
   pip install Pillow
   ```

2. Install the Waveshare e-ink display library following their official documentation

3. Ensure the DejaVu Sans font is available:
   ```bash
   sudo apt-get install fonts-dejavu-core
   ```

## Usage

Run the script directly:
```bash
python waveshare75_raspbi.py
```

The display will show:
- **Center**: Analog clock face with numbers at 12, 3, 6, 9 o'clock positions and line markers for other hours
- **Below analog clock**: Digital time display, centered and sized appropriately

## Display Layout

- **Screen Resolution**: 800×480 pixels
- **Analog Clock Center**: (600, 240) - vertically centered
- **Clock Radius**: 130 pixels
- **Digital Clock**: Centered below analog clock with 54px font
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
