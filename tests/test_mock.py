import json
from pathlib import Path
from unittest.mock import Mock, patch

import sunblock


# Mocking allows us to replace interfaces that require network
# connectivity or external infrastructure with a interface that mimics
# the return values, thus enabling testing of such code without having
# to setup aforesaid infrastructure. Here we mimic the requests.get()
# call to OpenMeteo.
@patch("sunblock.requests")
def test_fetch(mock_requests):
    loc = sunblock.Location(51.76, -1.24)
    with Path(__file__).with_name("openmeteo.json").open() as fp:
        data = json.load(fp)
        mock_requests.get.return_value = Mock(
            **{
                "status_code": 200,
                "json.return_value": data,
            }
        )
        res = sunblock.fetch(loc)
        mock_requests.get.assert_called_once()
        assert len(res["hourly"]["time"]) == 24 * 7  # hourly data for 7 days
