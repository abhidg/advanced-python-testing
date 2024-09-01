"Fixtures common to all tests"

import json
import pytest
from pathlib import Path

from sunblock import process


@pytest.fixture(scope="session")
def openmeteo_data():
    data = json.loads(Path(__file__).with_name("openmeteo.json").read_text())
    return process(data)
