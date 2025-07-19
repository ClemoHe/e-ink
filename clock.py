import math
from PIL import ImageDraw, ImageFont
from datetime import datetime

# Fonts and clock layout constants (can be customized or passed in)
FONT_DIGITAL_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_NUMBERS_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_DIGITAL_SIZE = 54
FONT_NUMBERS_SIZE = int(24 * 1.3)

CENTER_X, CENTER_Y = 600, 160
RADIUS = 130

font_digital = ImageFont.truetype(FONT_DIGITAL_PATH, FONT_DIGITAL_SIZE)
font_numbers = ImageFont.truetype(FONT_NUMBERS_PATH, FONT_NUMBERS_SIZE)

def draw_analog_clock(draw, center_x, center_y, radius, hour, minute, font_numbers, clock_marks="numbers"):
    # Clock face (bolder outer ring)
    for w in range(3, 0, -1):
        draw.ellipse((center_x - radius + w, center_y - radius + w, center_x + radius - w, center_y + radius - w), outline=0)

    # Draw hour marks: numbers or lines
    for hour_mark in range(12):
        angle = math.radians(hour_mark * 30 - 90)
        if clock_marks == "lines":
            # Draw a line for each hour mark
            outer_radius = radius * 0.95
            inner_radius = radius * 0.80
            x_outer = center_x + outer_radius * math.cos(angle)
            y_outer = center_y + outer_radius * math.sin(angle)
            x_inner = center_x + inner_radius * math.cos(angle)
            y_inner = center_y + inner_radius * math.sin(angle)
            draw.line((x_inner, y_inner, x_outer, y_outer), fill=0, width=3)
        else:
            # Draw numbers
            number_radius = radius * 0.85
            x_num = center_x + number_radius * math.cos(angle)
            y_num = center_y + number_radius * math.sin(angle)
            number = 12 if hour_mark == 0 else hour_mark
            text_width, text_height = draw.textsize(str(number), font=font_numbers)
            draw.text((x_num - text_width//2, y_num - text_height//2), str(number), font=font_numbers, fill=0)

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

def draw_digital_time(draw, center_x, center_y, radius, time_str, font_digital):
    text_width, text_height = draw.textsize(time_str, font=font_digital)
    digital_x = center_x - text_width // 2
    digital_y = center_y + radius + 65

    # Draw rounded border around digital clock
    border_padding = 15
    border_x1 = digital_x - border_padding
    border_y1 = digital_y - border_padding
    border_x2 = digital_x + text_width + border_padding
    border_y2 = digital_y + text_height + border_padding
    corner_radius = 10

    # Top and bottom horizontal lines
    draw.line((border_x1 + corner_radius, border_y1, border_x2 - corner_radius, border_y1), fill=0, width=2)
    draw.line((border_x1 + corner_radius, border_y2, border_x2 - corner_radius, border_y2), fill=0, width=2)
    # Left and right vertical lines
    draw.line((border_x1, border_y1 + corner_radius, border_x1, border_y2 - corner_radius), fill=0, width=2)
    draw.line((border_x2, border_y1 + corner_radius, border_x2, border_y2 - corner_radius), fill=0, width=2)
    # Corner arcs
    draw.arc((border_x1, border_y1, border_x1 + 2*corner_radius, border_y1 + 2*corner_radius), 180, 270, fill=0, width=2)
    draw.arc((border_x2 - 2*corner_radius, border_y1, border_x2, border_y1 + 2*corner_radius), 270, 360, fill=0, width=2)
    draw.arc((border_x1, border_y2 - 2*corner_radius, border_x1 + 2*corner_radius, border_y2), 90, 180, fill=0, width=2)
    draw.arc((border_x2 - 2*corner_radius, border_y2 - 2*corner_radius, border_x2, border_y2), 0, 90, fill=0, width=2)

    draw.text((digital_x, digital_y), time_str, font=font_digital, fill=0)
