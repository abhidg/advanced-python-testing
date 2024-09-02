"""
Find the next block of sun shining for N hours at your location
"""

import math
import datetime
from typing import Any, NamedTuple

import pandas as pd
import requests

CLEARISH_SKY_WMO_CODES = [0, 1]


class SunblockResult(NamedTuple):
    num_hours: int
    start: datetime.datetime | None
    mean_temp_celsius: float | None
    message: str

    def __str__(self):
        if self.message:
            return self.message
        return f"""Found sun block of {self.num_hours} hours, starting at:
{self.start}, mean temperature is {self.mean_temp_celsius:.1f}°C"""


class Location(NamedTuple):
    latitude: float
    longitude: float


# example locations
OXFORD = Location(51.75, -1.25)
NEWCASTLE = Location(54.98, -1.6)
BRIGHTON = Location(50.75, 0)


def openmeteo_api_url(loc: Location) -> str:
    return (
        f"https://api.open-meteo.com/v1/forecast?latitude={loc.latitude}&longitude={loc.longitude}"
        "&hourly=temperature_2m,precipitation,weather_code"
        "&daily=sunrise,sunset"
        "&temperature_unit=fahrenheit"
    )


def fetch(loc: Location) -> dict[str, Any] | None:
    # return json.loads(Path("openmeteo.json").read_text()
    res = requests.get(openmeteo_api_url(loc))
    return res.json() if res.status_code == 200 else None


def fahrenheit_to_celsius(temp: pd.Series | float) -> pd.Series | float:
    if isinstance(temp, float):
        if math.isnan(temp):
            raise ValueError("Temperature cannot be nan")
        if math.isinf(temp):
            raise ValueError("Temperature cannot be infinity")
        if temp < -459.67:
            raise ValueError(
                "Temperature below minimum fahrenheit temperature at absolute zero"
            )
    return 5 * (temp - 32) / 9


def process(data: dict[str, Any] | None) -> pd.DataFrame | None:
    "Processes OpenMeteo data to a dataframe"
    if data is None:
        return None
    sunrise_times = data["daily"]["sunrise"]
    sunset_times = data["daily"]["sunset"]
    hourly = data["hourly"]
    sunrise = sum([[x] * 24 for x in sunrise_times], [])
    sunset = sum([[x] * 24 for x in sunset_times], [])
    return pd.DataFrame(
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


def find_sun(data: pd.DataFrame, num_hours: int) -> SunblockResult:
    "Finds sun for `num_hours` in the data, after `day_start`"
    assert isinstance(num_hours, int), "num_hours should be an integer"
    if num_hours < 1:
        raise ValueError("Minimum num_hours is 1")
    if num_hours > 23:
        raise ValueError("Maximum sun block allowed is 23 hours")
    sunny = (
        (data.sunrise <= data.time)
        & (data.time <= data.sunset)
        & (data.weather_code.isin(CLEARISH_SKY_WMO_CODES))
    )
    sunny_coded = sunny.map(lambda x: "S" if x else " ").sum()
    idx = sunny_coded.find("S" * num_hours)
    if idx == -1:
        return SunblockResult(num_hours, None, None, "No sunny interval found")
    else:
        mean_temp = data.loc[idx : idx + num_hours].temperature_celsius.mean()
        return SunblockResult(
            num_hours,
            datetime.datetime.fromisoformat(data.loc[idx].time),
            mean_temp,
            "",
        )


if __name__ == "__main__":
    loc = NEWCASTLE
    data = fetch(loc)
    df = process(data)
    if isinstance(df, pd.DataFrame):
        print(find_sun(df, 2))
    else:
        print("Error fetching data for", loc)
