import time
import alarm
import board
from adafruit_magtag.magtag import MagTag

# ---- Config ----
LAT = 51.51
LON = -0.59

# Update every 30 minutes (battery-friendly)
SLEEP_SECONDS = 30 * 60

# Open-Meteo endpoint: current temp + precipitation probability (hourly)
URL = (
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude={LAT}&longitude={LON}"
    "&current=temperature_2m"
    "&hourly=precipitation_probability"
    "&forecast_days=1"
    "&timezone=Europe%2FLondon"
)

FONT = "/fonts/Arial-12.bdf"

# ---- Init MagTag ----
magtag = MagTag()

# Use built-in helpers (connects using settings.toml)
magtag.network.connect()

# Fetch JSON
r = magtag.network.requests.get(URL)
data = r.json()
r.close()

# Parse
temp_c = data["current"]["temperature_2m"]

# precipitation_probability is hourly array; take the first hour as "now-ish"
rain_prob = data["hourly"]["precipitation_probability"][0]

# ---- Display ----
magtag.graphics.set_background(0xFFFFFF)

magtag.add_text(
    text_font=FONT,
    text_position=(10, 5),
    text_color=0x000000,
)
magtag.set_text("Slough", 0)

magtag.add_text(
    text_font=FONT,
    text_position=(10, 25),
    text_color=0x000000
)
magtag.set_text(f"{temp_c:.1f}C", 1)

magtag.add_text(
    text_font=FONT,
    text_position=(10, 45),
    text_color=0x000000
)
magtag.set_text(f"Rain: {rain_prob:d}%", 2)

# ---- Deep sleep ----
time.sleep(2)  # let you see it update before sleeping
alarm.exit_and_deep_sleep_until_alarms(
    alarm.time.TimeAlarm(monotonic_time=time.monotonic() + SLEEP_SECONDS)
)