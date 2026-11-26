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