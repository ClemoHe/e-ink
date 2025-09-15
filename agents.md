# AI Agent Context - E-Ink Display Project

## Project Overview
This is a Python-based e-ink display system for Raspberry Pi that shows:
- **Weather forecast** (3 days: today, tomorrow, day after)
- **Analog and digital clock**
- **Pi-hole network statistics**

## Architecture & File Structure

### Main Files
- `waveshare75_raspbi.py` - Main application loop and display coordination
- `weather.py` - Weather API integration and forecast data
- `clock.py` - Clock rendering (analog and digital)
- `pihole.py` - Pi-hole statistics fetching and display
- `README.md` - User documentation
- `instructions.md` - Development coding guidelines

### Display Layout (800x480 e-ink screen)
```
┌─────────────────────────────────────────────────────┐
│ WEATHER (left)           CLOCK (right center)      │
│ Today:                   ┌─────────┐                │
│ - Morning: ...           │ Analog  │                │
│ - Noon: ...              │ Clock   │                │
│ - Evening: ...           │    12   │                │
│ Tomorrow:                │ 9   3   │                │
│ - Morning: ...           │    6    │                │
│ ...                      └─────────┘                │
│                          HH:MM (digital)           │
│                                                     │
│ PI-HOLE STATS (bottom left box)                    │
│ ┌─────────────────────────────────┐                │
│ │ Queries: xxx  Domains: xxx     │                │
│ │ Blocked: xxx  Status: xxx      │                │
│ └─────────────────────────────────┘                │
└─────────────────────────────────────────────────────┘
```

## Key Configuration
- **Environment Variables** (.env file):
  - `API_KEY` - Weather API key
  - `LAT`, `LON` - Location coordinates
  - `PIHOLE_URL` - Pi-hole server URL
  - `PIHOLE_PASSWORD` - Pi-hole admin password
  - `CLOCK_MARKS` - "numbers" or "lines" for clock face

## Important Technical Details

### Positioning & Spacing
- Weather text starts at (20, 20)
- Clock center at (CENTER_X, CENTER_Y) - defined in clock.py
- Pi-hole stats box at bottom left (20, height-100)
- Vertical spacing between weather blocks: 14px
- Gap after day labels: 28px

### PIL/Pillow Compatibility
- Uses `textsize()` instead of `textbbox()` for older PIL versions
- Custom rounded rectangle drawing for older PIL versions
- Compatible with Raspberry Pi's typical PIL installation

### Fonts
- Digital clock: DejaVu Sans 54px
- Weather: DejaVu Sans 24px
- Clock numbers: DejaVu Sans 24px
- Pi-hole stats: DejaVu Sans 22px

### Update Cycle
- Main loop runs every 60 seconds
- Weather data fetched once per hour
- Pi-hole stats fetched every cycle

## Common Modification Areas
1. **Spacing adjustments** - Look for `y +=` values in weather section
2. **Font sizes** - Font definitions at top of files
3. **Box dimensions** - `pihole_width`, `pihole_height` variables
4. **Position tweaks** - X,Y coordinate variables

## Dependencies
- `waveshare_epd` - E-ink display library
- `PIL` (Pillow) - Image processing
- `requests` - HTTP requests for APIs
- `python-dotenv` - Environment variable loading

## Error Handling
- Weather API failures fall back to cached data
- Pi-hole authentication uses session management
- Display errors don't crash the main loop
