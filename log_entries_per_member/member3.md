### Defect 4: Wrong nearest city in nearest_city
- **Symptom:** Earthquakes east of Mindanao are listed under a city in northern Luzon, more than 1,000 km away.
- **Cause:** In `quakewatch.py`, inside `nearest_city` (line 142), `events["longitude"]` and `events["latitude"]` were passed in swapped order to `haversine_km(lat1, lon1, lat2, lon2)`, corrupting the great-circle distance calculation.
- **Fix:** Swapped the `events` arguments in the `haversine_km(...)` call so `events["latitude"]` is passed first (`lat1`) and `events["longitude"]` second (`lon1`), matching `cities`.
- **Guarding tests:** `tests/test_integrate.py::test_nearest_city_of_known_events`
- **Evidence:** Ran `python -m pytest -k test_nearest_city_of_known_events -v` — failed before the fix (Mindanao event `2023-12-02 14:37` mapped to northern Luzon instead of `C10`) and passed all 3 parametrized cases after the fix.
- **Fixed by:** Member 3 (John Amon)

### Own test: 
- **Test:** 
- **What it checks:** 
- **Fails on baseline:** 
- **Passes on repaired code:** 
- **Written by:** Member 3 (John Amon)
