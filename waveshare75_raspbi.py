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

center_x, center_y = 600, 160  # Calculated for balanced 0.8cm spacing
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
            # Get text size for centering (compatible with older PIL versions)
            text_width, text_height = draw.textsize(str(number), font=font_numbers)
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
    # Get text size for centering (compatible with older PIL versions)
    text_width, text_height = draw.textsize(time_str, font=font_digital)
    digital_x = center_x - text_width // 2  # Center horizontally with analog clock
    digital_y = center_y + radius + 65  # Increased spacing to redistribute bottom space
    
    # Draw rounded border around digital clock (compatible with older PIL)
    border_padding = 15
    border_x1 = digital_x - border_padding
    border_y1 = digital_y - border_padding
    border_x2 = digital_x + text_width + border_padding
    border_y2 = digital_y + text_height + border_padding
    corner_radius = 10
    
    # Draw rounded rectangle using lines only (no filled rectangles)
    # Top and bottom horizontal lines
    draw.line((border_x1 + corner_radius, border_y1, border_x2 - corner_radius, border_y1), fill=0, width=2)  # Top
    draw.line((border_x1 + corner_radius, border_y2, border_x2 - corner_radius, border_y2), fill=0, width=2)  # Bottom
    
    # Left and right vertical lines
    draw.line((border_x1, border_y1 + corner_radius, border_x1, border_y2 - corner_radius), fill=0, width=2)  # Left
    draw.line((border_x2, border_y1 + corner_radius, border_x2, border_y2 - corner_radius), fill=0, width=2)  # Right
    
    # Corner arcs
    draw.arc((border_x1, border_y1, border_x1 + 2*corner_radius, border_y1 + 2*corner_radius), 180, 270, fill=0, width=2)  # Top-left
    draw.arc((border_x2 - 2*corner_radius, border_y1, border_x2, border_y1 + 2*corner_radius), 270, 360, fill=0, width=2)  # Top-right
    draw.arc((border_x1, border_y2 - 2*corner_radius, border_x1 + 2*corner_radius, border_y2), 90, 180, fill=0, width=2)   # Bottom-left
    draw.arc((border_x2 - 2*corner_radius, border_y2 - 2*corner_radius, border_x2, border_y2), 0, 90, fill=0, width=2)     # Bottom-right
    
    draw.text((digital_x, digital_y), time_str, font=font_digital, fill=0)

    # Minutenzeiger (shortened to not touch the circle)
    angle_min = math.radians(minute / 60 * 360 - 90)
    x_min = center_x + (radius * 0.85) * math.cos(angle_min)  # Shortened from radius to 0.85 * radius
    y_min = center_y + (radius * 0.85) * math.sin(angle_min)
    draw.line((center_x, center_y, x_min, y_min), fill=0, width=2)

    # Stundenzeiger
    angle_hour = math.radians((hour / 12 * 360 + minute / 60 * 30) - 90)
    x_hour = center_x + (radius * 0.6) * math.cos(angle_hour)
    y_hour = center_y + (radius * 0.6) * math.sin(angle_hour)
    draw.line((center_x, center_y, x_hour, y_hour), fill=0, width=4)

    epd.display(epd.getbuffer(Himage))

    # 1x pro Minute aktualisieren
    time.sleep(60)
