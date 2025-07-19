import requests
from datetime import datetime, timedelta

# Weather forecast font size (for reference, not used directly here)
WEATHER_FONT_SIZE = 24

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

    def get_for_time(target_date, target_hour):
        now = datetime.now()
        if target_date == now.date() and target_hour < now.hour:
            return "in the past"
        closest_entry = None
        min_diff = 24
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
