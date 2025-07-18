import os
import math
from waveshare_epd import epd7in5_V2
from PIL import Image, ImageDraw, ImageFont
import time
from datetime import datetime

epd = epd7in5_V2.EPD()
epd.init()

font_digital = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 72)

center_x, center_y = 600, 240  # Mittelpunkt für analoge Uhr (vertically centered)
radius = 130  # 30% larger than original 100

while True:
    now = datetime.now()
    time_str = now.strftime("%H:%M")
    minute = now.minute
    hour = now.hour % 12

    Himage = Image.new('1', (epd.width, epd.height), 255)
    draw = ImageDraw.Draw(Himage)

    # Weißer Hintergrund
    draw.rectangle((0, 0, epd.width, epd.height), fill=255)

    # Digitale Uhrzeit (links oben)
    draw.text((50, 50), time_str, font=font_digital, fill=0)

    # Analoge Uhr (rechts)
    # Ziffernblatt
    draw.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), outline=0)

    # Minutenzeiger
    angle_min = math.radians(minute / 60 * 360 - 90)
    x_min = center_x + radius * math.cos(angle_min)
    y_min = center_y + radius * math.sin(angle_min)
    draw.line((center_x, center_y, x_min, y_min), fill=0, width=2)

    # Stundenzeiger
    angle_hour = math.radians((hour / 12 * 360 + minute / 60 * 30) - 90)
    x_hour = center_x + (radius * 0.6) * math.cos(angle_hour)
    y_hour = center_y + (radius * 0.6) * math.sin(angle_hour)
    draw.line((center_x, center_y, x_hour, y_hour), fill=0, width=4)

    epd.display(epd.getbuffer(Himage))

    # 1x pro Minute aktualisieren
    time.sleep(60)
