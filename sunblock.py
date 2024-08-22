"""
Find the next block of sun shining for N hours at your location
"""

import datetime
from typing import Any, NamedTuple

import pandas as pd
import requests


class SunblockResult(NamedTuple):
    start: datetime.datetime | None
    mean_temp_celsius: float | None
    message: str


class Location(NamedTuple):
    latitude: float
    longitude: float


# example locations
OXFORD = Location(51.75, -1.25)
NEWCASTLE = Location(54.98, -1.61)
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
            "temperature_fahrenheit": hourly["temperature_2m"],
            "precipitation_mm": hourly["precipitation"],
            "weather_code": hourly["weather_code"],
        }
    )


def find_sun(data: pd.DataFrame, num_hours: int) -> SunblockResult:
    "Finds sun for `num_hours` in the data, after `day_start`"
    assert (
        isinstance(num_hours, int) and 0 < num_hours < 23
    ), "Number of hours must be between 0 and 23"
    sunny = (
        (data.sunrise <= data.time)
        & (data.time <= data.sunset)
        & (data.weather_code == 0)
    )
    sunny_coded = sunny.map(lambda x: "S" if x else " ").sum()
    idx = sunny_coded.find("S" * num_hours)
    if idx == -1:
        return SunblockResult(None, None, "No sunny interval found")
    else:
        mean_temp = data.loc[idx : idx + num_hours].temperature_fahrenheit.mean()
        return SunblockResult(data.loc[idx].time, mean_temp, "")


def sun_precip_times(data: pd.DataFrame) -> pd.DataFrame:
    "Report total sunshine time and total precipitation amount in mm"
    pass


if __name__ == "__main__":
    loc = BRIGHTON
    data = fetch(loc)
    df = process(data)
    if isinstance(df, pd.DataFrame):
        print(find_sun(df, 2))
    else:
        print("Error fetching data for", loc)
