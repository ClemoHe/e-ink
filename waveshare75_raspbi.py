import os
from dotenv import load_dotenv
import math
import requests
from waveshare_epd import epd7in5_V2
from PIL import Image, ImageDraw, ImageFont
import time
from datetime import datetime, timedelta

epd = epd7in5_V2.EPD()
epd.init()

font_digital = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 54)  # 25% smaller
font_numbers = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", int(24 * 1.3))  # For clock face numbers
# Weather forecast font (original size)
font_weather = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)

center_x, center_y = 600, 160  # Calculated for balanced 0.8cm spacing
radius = 130  # 30% larger than original 100


# Load API key from .env file
load_dotenv()
api_key = os.getenv("API_KEY")


def get_forecast(api_key, lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if 'list' not in data:
        print("Weather API error:", data)
        return {
            "Today": {"Morning": "N/A", "Noon": "N/A", "Evening": "N/A"},
            "Tomorrow": {"Morning": "N/A", "Noon": "N/A", "Evening": "N/A"},
            "Day after": {"Morning": "N/A", "Noon": "N/A", "Evening": "N/A"}
        }
    forecasts = data['list']

    # Helper to get forecast for a specific day and hour
    def get_for_time(target_date, target_hour):
        now = datetime.now()
        # If today and the slot is in the past, show 'in the past'
        if target_date == now.date() and target_hour < now.hour:
            return "in the past"
        closest_entry = None
        min_diff = 24  # max possible hour diff
        for entry in forecasts:
            dt = datetime.fromtimestamp(entry['dt'])
            if dt.date() == target_date:
                diff = abs(dt.hour - target_hour)
                if diff < min_diff:
                    min_diff = diff
                    closest_entry = entry
        if closest_entry:
            temp = round(closest_entry['main']['temp'])
            desc = closest_entry['weather'][0]['description'].capitalize()
            return f"{temp}°C, {desc}"
        return "N/A"

    today = datetime.now().date()
    result = {}
    for offset, label in zip([0, 1, 2], ["Today", "Tomorrow", "Day after"]):
        day = today + timedelta(days=offset)
        result[label] = {
            "Morning": get_for_time(day, 9),
            "Noon": get_for_time(day, 12),
            "Evening": get_for_time(day, 18)
        }
    return result





while True:
    now = datetime.now()
    time_str = now.strftime("%H:%M")
    minute = now.minute
    hour = now.hour % 12

    # In your main loop, before drawing:
    lat = 50.2577
    lon = 10.9660
    forecast = get_forecast(api_key, lat, lon)

    Himage = Image.new('1', (epd.width, epd.height), 255)
    draw = ImageDraw.Draw(Himage)

    # White background
    draw.rectangle((0, 0, epd.width, epd.height), fill=255)

    # Draw weather info on the left half
    left_x = 20
    y = 20
    font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
    # Use original weather font size
    # font_weather is already defined globally

    for day_label in ["Today", "Tomorrow", "Day after"]:
        draw.text((left_x, y), f"{day_label}:", font=font_title, fill=0)
        y += 32
        for part in ["Morning", "Noon", "Evening"]:
            draw.text((left_x + 10, y), f"{part}: {forecast[day_label][part]}", font=font_weather, fill=0)
            y += 28
        y += 10  # Extra space between days




    # Analog clock (right)
    # Clock face (bolder outer ring)
    for w in range(3, 0, -1):
        draw.ellipse((center_x - radius + w, center_y - radius + w, center_x + radius - w, center_y + radius - w), outline=0)

    # Hour numbers only (no tick marks or lines)
    for hour_mark in range(12):
        angle = math.radians(hour_mark * 30 - 90)  # 30 degrees per hour
        number_radius = radius * 0.85
        x_num = center_x + number_radius * math.cos(angle)
        y_num = center_y + number_radius * math.sin(angle)
        number = 12 if hour_mark == 0 else hour_mark
        text_width, text_height = draw.textsize(str(number), font=font_numbers)
        draw.text((x_num - text_width//2, y_num - text_height//2), str(number), font=font_numbers, fill=0)

    # Digital time (below analog clock)
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

    # Minute hand (shortened to not touch the circle, thicker)
    angle_min = math.radians(minute / 60 * 360 - 90)
    x_min = center_x + (radius * 0.85) * math.cos(angle_min)
    y_min = center_y + (radius * 0.85) * math.sin(angle_min)
    draw.line((center_x, center_y, x_min, y_min), fill=0, width=5)

    # Hour hand (thicker)
    angle_hour = math.radians((hour / 12 * 360 + minute / 60 * 30) - 90)
    x_hour = center_x + (radius * 0.6) * math.cos(angle_hour)
    y_hour = center_y + (radius * 0.6) * math.sin(angle_hour)
    draw.line((center_x, center_y, x_hour, y_hour), fill=0, width=8)

    epd.display(epd.getbuffer(Himage))

    # Update once per minute
    time.sleep(60)
