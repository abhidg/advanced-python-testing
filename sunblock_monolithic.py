"""
Find the next block of sun shining for N hours at your location
"""

import sys
import pandas as pd
import datetime
import requests

CLEARISH_SKY_WMO_CODES = [0, 1]


# example locations
OXFORD = (51.75, -1.25)
NEWCASTLE = (54.98, -1.61)
BRIGHTON = (50.75, 0)

loc = NEWCASTLE
sunblock_hours = 2  # try to get a 2 hour sun block


def fahrenheit_to_celsius(temp):
    return 5 * (temp - 32) / 9


# Fetch data from OpenMeteo
res = requests.get(
    f"https://api.open-meteo.com/v1/forecast?latitude={loc[0]}&longitude={loc[1]}"
    "&hourly=temperature_2m,precipitation,weather_code"
    "&daily=sunrise,sunset"
    "&temperature_unit=fahrenheit"
)

if res.status_code != 200:
    print("Error fetching from OpenMeteo")
    sys.exit(1)

# Process data, creating a dataframe that can be filtered
data = res.json()
sunrise_times = data["daily"]["sunrise"]
sunset_times = data["daily"]["sunset"]
hourly = data["hourly"]
sunrise = sum([[x] * 24 for x in sunrise_times], [])
sunset = sum([[x] * 24 for x in sunset_times], [])
df = pd.DataFrame(
    {
        "time": hourly["time"],
        "sunrise": sunrise,
        "sunset": sunset,
        "temperature_celsius": fahrenheit_to_celsius(
            pd.Series(hourly["temperature_2m"])
        ),
        "precipitation_mm": hourly["precipitation"],
        "weather_code": hourly["weather_code"],
    }
)

NOW = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
assert (
    isinstance(sunblock_hours, int) and 0 < sunblock_hours < 23
), "Number of hours must be between 0 and 23"

# Sunny when it is day time and the sky is clear or partly cloudy
sunny = (
    (df.sunrise <= df.time)
    & (df.time > NOW)
    & (df.time <= df.sunset)
    & (df.weather_code.isin(CLEARISH_SKY_WMO_CODES))
)
sunny_coded = sunny.map(lambda x: "S" if x else " ").sum()

# Use substring search to find first instance of sun block
if (idx := sunny_coded.find("S" * sunblock_hours)) == -1:
    print("No sunny interval found")
else:
    mean_temp = df.loc[idx : idx + sunblock_hours].temperature_celsius.mean()
    print(
        f"""Found sun block of {sunblock_hours} hours, starting at:
{df.loc[idx].time}, mean temperature is {mean_temp:.1f}°C"""
    )
