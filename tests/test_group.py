# GROUP TESTS 

import logging
import pandas as pd 
import pytest
import responses 
import quakewatch as qw 
from quakewatch import mag_class
# MEMBER 1: CAPLOG TEST


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


# MEMBER 4: EXTRA TEST


# MEMBER 5: EXTRA TEST