import os
import math
from waveshare_epd import epd7in5_V2
from PIL import Image, ImageDraw, ImageFont
import time
from datetime import datetime

epd = epd7in5_V2.EPD()
epd.init()

font_digital = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 54)  # 25% smaller
font_numbers = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)  # For clock face numbers

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

    # Analoge Uhr (rechts)
    # Ziffernblatt
    draw.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), outline=0)
    
    # Hour markings and numbers
    for hour_mark in range(12):
        angle = math.radians(hour_mark * 30 - 90)  # 30 degrees per hour
        
        if hour_mark in [0, 3, 6, 9]:  # Numbers at 12, 3, 6, 9
            # Calculate position for numbers
            number_radius = radius * 0.85
            x_num = center_x + number_radius * math.cos(angle)
            y_num = center_y + number_radius * math.sin(angle)
            
            # Display numbers (12, 3, 6, 9)
            number = 12 if hour_mark == 0 else hour_mark
            # Get text size for centering
            bbox = draw.textbbox((0, 0), str(number), font=font_numbers)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            draw.text((x_num - text_width//2, y_num - text_height//2), str(number), font=font_numbers, fill=0)
        else:  # Lines for other hour marks
            # Outer point
            x_outer = center_x + radius * 0.95 * math.cos(angle)
            y_outer = center_y + radius * 0.95 * math.sin(angle)
            # Inner point
            x_inner = center_x + radius * 0.85 * math.cos(angle)
            y_inner = center_y + radius * 0.85 * math.sin(angle)
            draw.line((x_inner, y_inner, x_outer, y_outer), fill=0, width=2)

    # Digitale Uhrzeit (below analog clock)
    # Get text size for centering
    bbox = draw.textbbox((0, 0), time_str, font=font_digital)
    text_width = bbox[2] - bbox[0]
    digital_x = center_x - text_width // 2  # Center horizontally with analog clock
    digital_y = center_y + radius + 30  # Position below analog clock
    draw.text((digital_x, digital_y), time_str, font=font_digital, fill=0)

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
