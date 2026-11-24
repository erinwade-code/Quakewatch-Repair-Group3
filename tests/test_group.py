# GROUP TESTS 

import logging
import pandas as pd 
import pytest
import responses 
import quakewatch as qw 

# MEMBER 1: CAPLOG TEST


# MEMBER 2: PARAMETRIZE TEST


# MEMBER 3: FAKE API TEST
def test_fake_api_pagination():
    '''A fake API test with responses'''
    fake_event_1 = {
    "id": "fake1",
    "properties": {
        "time": 1701527820000,   
        "mag": 6.2,
        "magType": "mww",
        "place": "10 km E of Test, Philippines",
    },
    "geometry": {
        "coordinates": [126.42, 8.53, 40.0] 
    },
    }

    fake_event_2 = {
    "id": "fake2",
    "properties": {
        "time": 1701528000000,
        "mag": 4.2,
        "magType": "wmm",
        "place": "20 km E of Test, Philippines",
    },
    "geometry": {
        "coordinates": [123.42, 4.53, 20.0]
    },
    }

    fake_event_3 = {
    "id": "fake3",
    "properties": {
        "time": 1701527900000,
        "mag": 2.2,
        "magType": "wmw",
        "place": "60 km E of Test, Philippines",
    },
    "geometry": {
        "coordinates": [123.2, 4.23, 25.0]
    },
    }

    page1 = {"type": "FeatureCollection", "features": [fake_event_1, fake_event_2]}
    page2 = {"type": "FeatureCollection", "features": [fake_event_3]}

    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, f"{qw.BASE}/fdsnws/event/1/query", json=page1, status=200)
        rsps.add(responses.GET, f"{qw.BASE}/fdsnws/event/1/query", json=page2, status=200)
        dfr = qw.fetch_range("2023-01-01", "2023-01-02", limit=2)
        
        assert len(rsps.calls) == 2
        assert rsps.calls[0].request.params["offset"] == "1"
        assert rsps.calls[1].request.params["offset"] == "3"

    assert len(dfr) == 3
    assert list(dfr["id"]) == ["fake1", "fake2", "fake3"]

# MEMBER 4: EXTRA TEST


# MEMBER 5: EXTRA TEST