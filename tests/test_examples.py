import json
import pytest
import datetime
from pathlib import Path

from numpy.testing import assert_approx_equal

from sunblock import (
    fetch,
    Location,
    openmeteo_api_url,
    fahrenheit_to_celsius,
    process,
    find_sun,
    SunblockResult,
    NEWCASTLE,
)


def test_openmeteo_url():
    assert openmeteo_api_url(Location(1, -1)) == (
        "https://api.open-meteo.com/v1/forecast?latitude=1&longitude=-1"
        "&hourly=temperature_2m,precipitation,weather_code"
        "&daily=sunrise,sunset"
        "&temperature_unit=fahrenheit"
    )


# This will fail if there is no network connection or if OpenMeteo is down
def test_fetch_network():
    data = fetch(NEWCASTLE)
    print(data)
    assert_approx_equal(data["latitude"], NEWCASTLE[0])
    assert_approx_equal(data["longitude"], NEWCASTLE[1])
    assert len(data["hourly"]["time"]) == 24 * 7


@pytest.mark.parametrize(
    "fahrenheit,expected_celsius",
    [
        (212, 100),
        (32, 0),
    ],
)
def test_fahrenheit_to_celsius(fahrenheit, expected_celsius):
    assert fahrenheit_to_celsius(fahrenheit) == expected_celsius


def test_process(openmeteo_data):
    # do not check actual details, only lengths
    # TODO: use snapshot testing here
    assert (
        len(openmeteo_data) == 24 * 7
    )  # OpenMeteo reports 7 days data, on a hourly basis

    # sunrise and sunset data repeat in 24 hour blocks
    # checks first 24 rows to verify that sunrise and sunset are equal
    assert len(openmeteo_data.iloc[:24].sunrise.unique()) == 1
    assert len(openmeteo_data.iloc[:24].sunset.unique()) == 1


def test_find_sun(openmeteo_data):
    block = find_sun(openmeteo_data, num_hours=3)
    assert_approx_equal(block.mean_temp_celsius, 19.916666666666668)
    assert (block.num_hours, block.start, block.message) == (
        3,
        datetime.datetime.fromisoformat("2024-08-23T11:00"),
        "",
    )


def test_find_sun_not_found(openmeteo_data):
    block = find_sun(openmeteo_data, num_hours=4)
    assert block == (4, None, None, "No sunny interval found")


@pytest.mark.parametrize(
    "block,printed_block",
    [
        (
            SunblockResult(5, None, None, "No sunny interval found"),
            "No sunny interval found",
        ),
        (
            SunblockResult(2, datetime.datetime(2024, 8, 24, 11, 0), 11.199999999, ""),
            """Found sun block of 2 hours, starting at:
2024-08-24 11:00:00, mean temperature is 11.2°C""",
        ),
    ],
)
def test_sunblock_pretty_print(block, printed_block):
    assert str(block) == printed_block
