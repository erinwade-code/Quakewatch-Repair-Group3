# Repair log: QuakeWatch (Group 3)

Course: DSA4153 Programming for Data Science, Week 15 Group Activity

**Starting point:** `python -m pytest -q .` gave 7 failed, 9 passed, 4 errors.
**End point:** 31 passed (the 20 supplied tests plus our own tests). See `pytest_output.txt`.

**Members**

| Member | Name |
| --- | --- |
| 1 | Erin Wade Acuna |
| 2 | Neo Carl Jacinto |
| 3 | John Amon |
| 4 | Lance Wesley Santos |
| 5 | Gabriel Dolar |

## Summary

| # | Defect | Fixed by | Guarding test |
| --- | --- | --- | --- |
| 1 | `KeyError: 'depth'` in `features_stage` | Member 1 (Erin Wade Acuna); also Member 4 (Lance Wesley Santos) | `test_features_stage_runs`, `test_depth_classes` |
| 2 | Strongest earthquake shown in wrong Manila time | Member 1 (Erin Wade Acuna); also Member 4 (Lance Wesley Santos) | `test_strongest_event_is_at_night_in_manila` |
| 3 | Magnitude 6.0 labelled Moderate | Member 2 (Neo Carl Jacinto) | `test_mag_class_edges`, `test_mag_class_boundaries` |
| 4 | Wrong nearest city | Member 3 (John Amon) | `test_nearest_city_of_known_events` |
| 5 | Second run duplicates every earthquake | Member 5 (Gabriel Dolar) | `test_second_load_adds_nothing`, `test_ids_stay_unique_after_two_loads` |
| 6 | Bad rows are not set aside | Member 2 (Neo Carl Jacinto), with the logging by Member 3 (John Amon) | `test_bad_rows_are_set_aside`, `test_rejected_rows_log_a_warning` |

---

## Defects

### Defect 1: KeyError in features_stage
- **Symptom:** `python run.py` stops with `KeyError: 'depth'` before the dashboard is written.
- **Cause:** `features_stage()` called `depth_class(t["depth"])`, but the column in the table is named `depth_km`, so pandas raised KeyError.
- **Fix:** changed `t["depth"]` to `t["depth_km"]` in `features_stage()`.
- **Guarding tests:** `test_features_stage_runs` and `test_depth_classes` (tests/test_features.py).
- **Evidence:** pytest went from 7 failed, 9 passed, 4 errors to 9 failed, 11 passed, 0 errors. Failures rose because 4 tests that used to crash at the KeyError could now run, and two of them exposed defects 2 and 3.
- **Fixed by:** Member 1 (Erin Wade Acuna)

### Defect 2: Strongest earthquake shown in wrong Manila time
- **Symptom:** The dashboard said the strongest earthquake struck at 14:37 Manila time on 2 Dec 2023, but the news reported 10:37 PM (22:37).
- **Cause:** `t["time"].dt.tz_localize(None).dt.tz_localize("Asia/Manila")` removed the UTC label and attached Manila to the same clock reading, so the time was relabelled and not converted. The result was 8 hours off.
- **Fix:** replaced it with `t["time"].dt.tz_convert("Asia/Manila")`.
- **Guarding test:** `test_strongest_event_is_at_night_in_manila` (tests/test_features.py).
- **Evidence:** the test failed with `'2023-12-02 14:37' == '2023-12-02 22:37'` before the fix and passes after. pytest went from 9 failed, 11 passed to 8 failed, 12 passed, 0 errors.
- **Fixed by:** Member 1 (Erin Wade Acuna)

### Defect 3: Magnitude 6.0 labelled Moderate
- **Symptom:** The dashboard labelled a magnitude 6.0 earthquake as Moderate, but the USGS calls 6.0 to 6.9 Strong.
- **Cause:** `MAG_BINS = [4.95, 6.05, 6.95, 7.95, 10]` used offset edges, and `pd.cut` includes the right edge of each bin by default. So 6.0 fell in (4.95, 6.05] and was labelled Moderate, and 6.96 to 6.99 was labelled Major.
- **Fix:** replaced the bins with `MAG_BINS = [5, 6, 7, 8, np.inf]` and added `right=False` to `pd.cut(...)` in `mag_class`, so each class includes its lower edge.
- **Guarding tests:** `test_mag_class_edges` (tests/test_features.py) and `test_mag_class_boundaries` (tests/test_group.py).
- **Evidence:** the test failed with `assert 'Moderate' == 'Strong'` before the fix and passes after. `test_mag_class_edges[6.0-Strong]` was one of the 7 failures in our first run.
- **Fixed by:** Member 2 (Neo Carl Jacinto)

### Defect 4: Wrong nearest city in nearest_city
- **Symptom:** Earthquakes east of Mindanao are listed under a city in northern Luzon, more than 1,000 km away.
- **Cause:** In `quakewatch.py`, inside `nearest_city` (line 142), `events["longitude"]` and `events["latitude"]` were passed in swapped order to `haversine_km(lat1, lon1, lat2, lon2)`, corrupting the great-circle distance calculation.
- **Fix:** swapped the `events` arguments in the `haversine_km(...)` call so `events["latitude"]` is passed first (`lat1`) and `events["longitude"]` second (`lon1`), matching `cities`.
- **Guarding test:** `tests/test_integrate.py::test_nearest_city_of_known_events`
- **Evidence:** `python -m pytest -k test_nearest_city_of_known_events -v` failed before the fix (the Mindanao event `2023-12-02 14:37` mapped to northern Luzon instead of `C10`) and passed all 3 parametrized cases after the fix.
- **Fixed by:** Member 3 (John Amon)

### Defect 5: Running twice duplicates every earthquake
- **Symptom:** Running the pipeline twice duplicated every earthquake in `data/raw` (`new_rows` returned 462 again instead of 0).
- **Cause:** `quakewatch.py`, `load_new()`, lines 84 to 90: it always called `fetch_range(FIRST_DAY, until)` instead of checking `watermark()`, and did not filter out already-saved event IDs at the inclusive `starttime` boundary.
- **Fix:** updated `load_new()` to use `watermark()` as the start timestamp when raw files already exist, and to filter out any fetched rows whose `id` is already present in `data/raw` before saving.
- **Guarding tests:** `tests/test_acquire.py::test_second_load_adds_nothing`, `tests/test_acquire.py::test_ids_stay_unique_after_two_loads`, `tests/test_group.py::test_incremental_load_across_date_ranges_has_no_duplicates`
- **Evidence:** before the fix `test_second_load_adds_nothing` failed with `assert 462 == 0`. After the fix the second run gives `new_rows` of 0.
- **Fixed by:** Member 5 (Gabriel Dolar)

### Defect 6: Bad rows are not set aside
- **Symptom:** A planted bad row (`planted-bad-row`, depth -5 km) reached the clean data, and `rejects.csv` stayed empty.
- **Cause:** `split_by_contract()` called `CONTRACT.validate()` inside `try/except Exception: pass` and always returned `raw, raw.iloc[0:0]`. Every row counted as good and nothing was rejected.
- **Fix:** validate with `lazy=True`, catch `pa.errors.SchemaErrors`, use `err.failure_cases["index"]` to find the failing rows, and return the good rows and the rejected rows separately. The error is recorded with `log.exception` and the rejected rows with a `log.warning`. After the branches were merged, 2 tests still failed, so the integrator also fixed a typo in the `log.warning` call in `integrate()` (`and` instead of a comma) that raised a `TypeError`, and moved the rejected-rows WARNING inside `split_by_contract`.
- **Guarding tests:** `tests/test_integrate.py::test_bad_rows_are_set_aside` and `tests/test_group.py::test_rejected_rows_log_a_warning`
- **Evidence:** before the fix `test_bad_rows_are_set_aside` failed with `'planted-bad-row' not in {...}`. After the fix all 31 tests pass.
- **Fixed by:** Member 2 (Neo Carl Jacinto) during integration, building on Member 3's (John Amon) `log.exception` logging in `split_by_contract`.

### Member 4's entry: features_stage crashes and shows wrong local time (Defects 1 and 2)
Member 4 (Lance Wesley Santos) fixed these two problems on his own branch, `fix-defect-6`. His log calls it Defect 6. It describes the same two code changes as Defects 1 and 2 above.
- **Symptom:** The features stage crashed with `KeyError: 'depth'`. After that was fixed, the strongest event showed 14:37 instead of 22:37 local time.
- **Cause:** `features_stage` read a column called `depth`, but the cleaned data names it `depth_km`. Separately, the local time used `tz_localize(None).tz_localize("Asia/Manila")`, which relabels UTC clock times as Manila instead of converting them, so every hour was 8 hours off.
- **Fix:** Use `t["depth_km"]` and `t["time"].dt.tz_convert("Asia/Manila")`.
- **Guarding tests:** `test_depth_classes`, `test_strongest_event_is_at_night_in_manila`, and his own `test_features_manila_time_and_depth_class` in `tests/test_group.py`.
- **Fixed by:** Member 4 (Lance Wesley Santos)

---

## Our own tests (tests/test_group.py)

| Test | Tool | What it proves | Fails on the broken code? | Written by |
| --- | --- | --- | --- | --- |
| `test_mag_class_boundaries` | `parametrize` | Seven magnitudes at the class edges get the right class: 5.0 and 5.99 Moderate, 6.0 and 6.99 Strong, 7.0 and 7.99 Major, 8.0 Great. | Yes: 6.0, 6.99 and 7.99 fail on the old bins. | Member 2 (Neo Carl Jacinto) |
| `test_rejected_rows_log_a_warning` | `caplog` | A row with depth -5 km is rejected and a WARNING is logged on the `quakewatch` logger. | Yes: the old `split_by_contract` rejected nothing and logged nothing. | Member 1 (Erin Wade Acuna) |
| `test_fake_api_pagination` | fake API (`responses`) | `fetch_range()` paginates across multiple pages (`offset=1`, `offset=3` with `limit=2`), stops when a page has fewer than `limit` rows, and parses GeoJSON features into a table without hitting the real or practice server. | No: it tests pagination and parsing, which were not among the planted defects. | Member 3 (John Amon) |
| `test_incremental_load_across_date_ranges_has_no_duplicates` | `pytest` (`project` fixture) | Two consecutive `load_new()` calls (`2023-01-01`, then `2025-01-01`) only add new events and keep IDs unique (462 total). | Yes | Member 5 (Gabriel Dolar) |
| `test_features_manila_time_and_depth_class` | `pytest` | `features_stage` runs without `KeyError: 'depth'`, assigns depth classes from `depth_km`, and shows Manila local time by converting from UTC. | Yes: the old `features_stage` raised `KeyError: 'depth'` and had the time 8 hours off. | Member 4 (Lance Wesley Santos) |

## Logging we added

| Where | Level | Message | Why |
| --- | --- | --- | --- |
| `split_by_contract` | ERROR (`log.exception`) | Contract validation failed, with traceback | Records the caught validation error with the full traceback instead of silently ignoring it. |
| `split_by_contract` | WARNING | Number of rejected rows (written to `rejects.csv`) | Alerts that invalid rows were set aside while valid rows go on. |
| each stage | INFO | Row counts for acquire, integrate, features and report | Shows what each stage did. |
| `run.py` | file handler | Log written to `logs/run.log` | Keeps a record of every run for checking later. |

## Integration (final merge)

- Created the `final-merge` branch from `main` and merged each member's branch into it: `member1-defects-1-2`, `member1-test-1`, `fix-defect-3`, `member3-defects-4`, `fix-defect-5` and `fix-defect-6`.
- After merging, 2 tests still failed (bad rows were not set aside, and the rejected-rows WARNING was not logged). We fixed both in `quakewatch.py`, as described in Defect 6.
- Checked that the supplied tests and `tests/conftest.py` were not edited.
- Final result: `python -m pytest -q .` gave 31 passed.
- Ran `python run.py` twice. Both runs printed the same numbers, and the second run showed `new_rows` equal to 0. The output is in `logs/run.log`.

## One thing we learned about debugging

Fixing one defect sometimes uncovered another. The `KeyError: 'depth'` stopped four tests from running at all, and only after Defect 1 was fixed did the Manila time and magnitude defects show up. Running the tests after every change told us which change fixed which problem. We also learned that catching a broad `except Exception` and doing nothing hid Defect 6, so errors should be caught specifically and logged with `log.exception`.
