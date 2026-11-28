# Member 4: Lance Wesley Santos

## Defect 6: features_stage crashes and shows wrong local time
- **Symptom:** The features stage crashed with `KeyError: 'depth'`. After that was fixed, the strongest event showed 14:37 instead of 22:37 local time.
- **Cause:** `features_stage` read a column called `depth`, but the cleaned data names it `depth_km`. Separately, the local time used `tz_localize(None).tz_localize("Asia/Manila")`, which relabels UTC clock times as Manila instead of converting them, so every hour was 8 hours off.
- **Fix:** Use `t["depth_km"]` and `t["time"].dt.tz_convert("Asia/Manila")`.
- **Guarding test:** `test_depth_classes`, `test_strongest_event_is_at_night_in_manila`, and my `test_features_manila_time_and_depth_class` in `tests/test_group.py`.
- **Fixed by:** Lance Wesley Santos

