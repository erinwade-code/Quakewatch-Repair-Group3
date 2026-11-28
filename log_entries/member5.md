# Member 5 Repair Log Entry (Gabriel Dolar)

## Defect 5
| # | Symptom (what was wrong for the user) | Cause (file, function, line; why it was wrong) | Fix (what you changed) | Test that now guards it | Fixed by |
| --- | --- | --- | --- | --- | --- |
| 5 | Running the pipeline twice duplicated every earthquake in `data/raw` (`new_rows` returned 462 again instead of 0). | `quakewatch.py`, `load_new()`, lines 84–90: it always called `fetch_range(FIRST_DAY, until)` instead of checking `watermark()`, and did not filter out already-saved event IDs at the inclusive `starttime` boundary. | Updated `load_new()` to query `watermark()` for the `start` timestamp when raw files already exist and filter out any fetched rows whose `id` is already present in `data/raw` before saving. | `tests/test_acquire.py::test_second_load_adds_nothing`, `tests/test_acquire.py::test_ids_stay_unique_after_two_loads`, `tests/test_group.py::test_incremental_load_across_date_ranges_has_no_duplicates` | Gabriel Dolar |

## Test in `tests/test_group.py`
| Test name | Tool used (`parametrize`, fake API, `caplog`) | What it proves | Fails on the broken code? | Written by |
| --- | --- | --- | --- | --- |
| `test_incremental_load_across_date_ranges_has_no_duplicates` | `pytest` (`project` fixture) | Incremental calls to `load_new()` across two consecutive date windows (`2023-01-01` then `2025-01-01`) only append new events and preserve unique IDs (`462` total). | Yes | Gabriel Dolar |