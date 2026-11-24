### Defect 1: KeyError in features_stage
- **Symptom:** `python run.py` stops with `KeyError: 'depth'` before the dashboard is written.
- **Cause:** `features_stage()` called `depth_class(t["depth"])`, but the column in the table is named `depth_km`, so pandas raised KeyError.
- **Fix:** changed `t["depth"]` to `t["depth_km"]` in `features_stage()`.
- **Guarding tests:** `test_features_stage_runs` and `test_depth_classes` (tests/test_features.py).
- **Evidence:** pytest went from 7 failed, 9 passed, 4 errors to 9 failed, 11 passed, 0 errors. Failures rose because 4 tests that used to crash at the KeyError could now run, and two of them exposed defects #2 and #3.
- **Fixed by:** Member 1 (Erin Wade Acuna)

### Defect 2: Strongest earthquake shown in wrong Manila time
- **Symptom:** The dashboard said the strongest earthquake struck at 14:37 Manila time on 2 Dec 2023, but the news reported 10:37 PM (22:37).
- **Cause:** `t["time"].dt.tz_localize(None).dt.tz_localize("Asia/Manila")` removed the UTC label and attached Manila to the same clock reading, so the time was relabelled and not converted. The result was 8 hours off.
- **Fix:** replaced it with `t["time"].dt.tz_convert("Asia/Manila")`.
- **Guarding test:** `test_strongest_event_is_at_night_in_manila` (tests/test_features.py).
- **Evidence:** the test failed with `'2023-12-02 14:37' == '2023-12-02 22:37'` before the fix and passes after. pytest went from 9 failed, 11... to 8 failed, 12 passed, 0 errors.
- **Fixed by:** Member 1 (Erin Wade Acuna)