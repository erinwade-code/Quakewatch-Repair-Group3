# GROUP TESTS 

import logging
import pandas as pd 
import pytest
import responses 
import quakewatch as qw 
from quakewatch import mag_class
# MEMBER 1: CAPLOG TEST
def test_rejected_rows_log_a_warning(caplog):
    """A row with depth -5 km must be rejected AND logged as a WARNING."""
    raw = pd.DataFrame({
        "id": ["ok1", "bad1"],
        "time": pd.to_datetime(["2024-01-01", "2024-01-02"], utc=True),
        "latitude": [14.5, 14.5],
        "longitude": [121.0, 121.0],
        "depth_km": [10.0, -5.0],
        "mag": [5.5, 5.5],
        "magType": ["mww", "mww"],
        "place": ["test A", "test B"],
    })
    with caplog.at_level(logging.WARNING, logger="quakewatch"):
        good, rejected = qw.split_by_contract(raw)
    assert len(good) == 1
    assert len(rejected) == 1
    assert any(r.levelno == logging.WARNING for r in caplog.records)

# MEMBER 2: PARAMETRIZE TEST
@pytest.mark.parametrize("mag, expected", [
    (5.0, "Moderate"),
    (5.99, "Moderate"),
    (6.0, "Strong"),     # broken code: Moderate
    (6.99, "Strong"),    # broken code: Major
    (7.0, "Major"),
    (7.99, "Major"),     # broken code: Great
    (8.0, "Great"),
])
def test_mag_class_boundaries(mag, expected):
    assert str(mag_class(pd.Series([mag])).iloc[0]) == expected

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
def test_features_manila_time_and_depth_class(loaded):
    """features_stage must read depth_km and convert UTC to Manila time (UTC+8)."""
    qw.integrate()
    feat = qw.features_stage()

    # Defect: used to crash with KeyError: 'depth'
    assert "depth_class" in feat.columns
    assert set(feat["depth_class"]) <= {"shallow", "intermediate", "deep"}

    # Defect: the old tz_localize relabeled UTC as Manila, so the offset was 0 hours
    offset = feat["local"].dt.tz_localize(None) - feat["time"].dt.tz_localize(None)
    assert (offset == pd.Timedelta(hours=8)).all()

# MEMBER 5: EXTRA TEST
def test_incremental_load_across_date_ranges_has_no_duplicates(project):
    first_count = qw.load_new(until="2023-01-01")
    second_count = qw.load_new(until="2025-01-01")
    raw = qw.read_raw()
    assert first_count > 0
    assert second_count > 0
    assert first_count + second_count == 462
    assert len(raw) == 462
    assert raw["id"].is_unique