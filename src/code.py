import time
import alarm
import displayio
from adafruit_magtag.magtag import MagTag

from util.datetime import argmin_time, split_datetime

SCR_HEIGHT = 128
SCR_WIDTH = 296

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

FONT_BOLD = "/fonts/Arial-Bold-12.pcf"
FONT = "/fonts/Arial-12.bdf"

# ---- Init MagTag ----
magtag = MagTag()
display = magtag.graphics.display

# Use built-in helpers (connects using settings.toml)
magtag.network.connect()

# Fetch JSON
r = magtag.network.requests.get(URL)
data = r.json()
r.close()

root = magtag.graphics.root_group

bg_bmp = displayio.OnDiskBitmap("/bmp/bg.bmp")
bg = displayio.TileGrid(bg_bmp, pixel_shader=bg_bmp.pixel_shader)
root.append(bg)

therm_x = 65
therm_y = 30

icon_bmp = displayio.OnDiskBitmap("/bmp/therm.bmp")
icon = displayio.TileGrid(
    icon_bmp, pixel_shader=icon_bmp.pixel_shader, x=therm_x, y=therm_y)
root.append(icon)

drop_x = 165
drop_y = 30

icon_bmp = displayio.OnDiskBitmap("/bmp/drop.bmp")
icon = displayio.TileGrid(
    icon_bmp, pixel_shader=icon_bmp.pixel_shader, x=drop_x, y=drop_y)
root.append(icon)

temp_c = int(round(float(data["current"]["temperature_2m"])))
unit = data["current_units"]["temperature_2m"]

hour_idx = argmin_time(data["current"]["time"], data["hourly"]["time"])

rain_prob = data["hourly"]["precipitation_probability"][hour_idx]

text_idx = 0

magtag.add_text(
    text_font=FONT_BOLD,
    text_position=(therm_x+25, therm_y+5),
    text_color=0x000000,
)
magtag.set_text(f"{temp_c} {unit}", text_idx, auto_refresh=False)

text_idx += 1

magtag.add_text(
    text_font=FONT_BOLD,
    text_position=(drop_x+30, drop_y+5),
    text_color=0x000000
)
magtag.set_text(f"{rain_prob:d}%", text_idx, auto_refresh=False)

text_idx += 1

magtag.add_text(
    text_font=FONT,
    text_position=(20, SCR_HEIGHT-30),
    text_color=0x000000
)

date_now, time_now = split_datetime(data["current"]["time"])
magtag.set_text(
    f"Last updated: {time_now} {date_now}", text_idx, auto_refresh=False)

display.root_group = root
magtag.refresh()

# ---- Deep sleep ----
time.sleep(2)  # let you see it update before sleeping
alarm.exit_and_deep_sleep_until_alarms(
    alarm.time.TimeAlarm(monotonic_time=time.monotonic() + SLEEP_SECONDS)
)
