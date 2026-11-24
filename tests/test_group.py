# GROUP TESTS 

import logging
import pandas as pd 
import pytest
import responses 
import quakewatch as qw 

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


# MEMBER 3: FAKE API TEST


# MEMBER 4: EXTRA TEST


# MEMBER 5: EXTRA TEST