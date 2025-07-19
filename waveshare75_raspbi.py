
import os
from dotenv import load_dotenv
import time
import locale
import pprint
from datetime import datetime, timedelta
import os
from waveshare_epd import epd7in5_V2
from PIL import Image, ImageDraw, ImageFont
from clock import draw_analog_clock, draw_digital_time, font_digital, font_numbers, CENTER_X, CENTER_Y, RADIUS
from weather import get_forecast

epd = epd7in5_V2.EPD()
epd.init()



# Weather forecast font (original size)
font_weather = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)

locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')

# Load API Key, lat, long from .env file
load_dotenv()

clock_marks = os.getenv("CLOCK_MARKS", "numbers").lower()  # 'numbers' or 'lines'
print(f"CLOCK_MARKS from .env: '{clock_marks}'")


pprint.pprint(dict(os.environ))
api_key = os.getenv("API_KEY")
lat = float(os.getenv("LAT"))
lon = float(os.getenv("LON"))

while True:
    now = datetime.now()
    time_str = now.strftime("%H:%M")
    minute = now.minute
    hour = now.hour % 12

    forecast = get_forecast(api_key, lat, lon)

    Himage = Image.new('1', (epd.width, epd.height), 255)
    draw = ImageDraw.Draw(Himage)

    # White background
    draw.rectangle((0, 0, epd.width, epd.height), fill=255)

    # Draw weather info on the left half
    left_x = 20
    y = 20
    font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)

    labels = []
    today = datetime.now().date()
    for offset, forecast_key in zip(range(3), ["Today", "Tomorrow", "Day after"]):
        day = today + timedelta(days=offset)
        label = day.strftime('%A')
        labels.append((label, forecast_key))

    for label, forecast_key in labels:
        draw.text((left_x, y), f"{label}:", font=font_title, fill=0)
        y += 32
        for part in ["Morning", "Noon", "Evening"]:
            draw.text((left_x + 10, y), f"{part}: {forecast[forecast_key][part]}", font=font_weather, fill=0)
            y += 28
        y += 10

    # Draw analog clock (right)
    draw_analog_clock(draw, CENTER_X, CENTER_Y, RADIUS, hour, minute, font_numbers, clock_marks)

    # Draw digital time (below analog clock)
    draw_digital_time(draw, CENTER_X, CENTER_Y, RADIUS, time_str, font_digital)

    epd.display(epd.getbuffer(Himage))
    time.sleep(60)
    print('Test')
    # Minute hand (shortened to not touch the circle, thicker)
