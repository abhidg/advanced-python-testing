import json
from pathlib import Path

from sunblock import process


def test_process(snapshot):
    data = json.loads(Path(__file__).with_name("openmeteo.json").read_text())
    assert process(data).to_csv(index=False) == snapshot
