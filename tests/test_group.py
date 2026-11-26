# GROUP TESTS 

import logging
import pandas as pd 
import pytest
import responses 
import quakewatch as qw 

# MEMBER 1: CAPLOG TEST


# MEMBER 2: PARAMETRIZE TEST


# MEMBER 3: FAKE API TEST


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