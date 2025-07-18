# E-Ink Digital Clock Display

A Python-based digital clock application for Waveshare 7.5-inch e-ink displays, designed to run on Raspberry Pi.

## Overview

This project creates a dual-format clock display that shows both digital and analog time on an e-ink screen. The display updates every minute and is perfect for a low-power, always-on desktop clock.

## Features

- **Digital Clock**: Large, clear time display in HH:MM format
- **Analog Clock**: Traditional clock face with hour and minute hands
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
- **Left side**: Digital time in large font (top-left corner)
- **Right side**: Analog clock face with moving hands (vertically centered)

## Display Layout

- **Screen Resolution**: 800×480 pixels
- **Digital Clock Position**: (50, 50) from top-left
- **Analog Clock Center**: (600, 240) - centered in right half
- **Clock Radius**: 130 pixels
- **Background**: White
- **Text/Graphics**: Black

## Code Structure

- **Initialization**: Sets up the e-ink display and loads fonts
- **Main Loop**: Continuously updates the display every minute
- **Time Calculation**: Converts current time to both digital and analog formats
- **Drawing**: Creates the visual elements using PIL's drawing functions

## Customization

You can easily modify:
- Clock positions by changing `center_x`, `center_y` coordinates
- Clock size by adjusting the `radius` value
- Font size by modifying the font loading parameters
- Update frequency by changing the `time.sleep(60)` value

## Notes

- The analog clock uses 12-hour format
- Hour hand length is 60% of the minute hand for traditional appearance
- The display is optimized for the monochrome e-ink format
- Updates are intentionally limited to once per minute to preserve display lifespan
