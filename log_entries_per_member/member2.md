### Defect 3: Magnitude 6.0 labelled Moderate
- **Symptom:** The dashboard labelled a magnitude 6.0 earthquake as Moderate, but the USGS calls 6.0 to 6.9 Strong.
- **Cause:** `MAG_BINS = [4.95, 6.05, 6.95, 7.95, 10]` used offset edges, and `pd.cut` includes the right edge of each bin by default. So 6.0 fell in (4.95, 6.05] and was labelled Moderate, and 6.96 to 6.99 was labelled Major.
- **Fix:** replaced the bins with `MAG_BINS = [5, 6, 7, 8, np.inf]` and added `right=False` to `pd.cut(...)` in `mag_class`, so each class includes its lower edge.
- **Guarding test:** `test_mag_class_edges` (tests/test_features.py) and `test_mag_class_boundaries` (tests/test_group.py).
- **Evidence:** the test failed with `assert 'Moderate' == 'Strong'` before the fix and passes after. [PASTE pytest counts before and after, for example "X failed, Y passed" to "Z passed"]
- **Fixed by:** Member 2 (Neo Carl Jacinto)

### Own test: parametrize
- **Test:** `test_mag_class_boundaries` in tests/test_group.py
- **What it checks:** seven magnitudes at the class edges get the right class: 5.0 and 5.99 Moderate, 6.0 and 6.99 Strong, 7.0 and 7.99 Major, 8.0 Great.
- **Fails on baseline:** yes, the cases 6.0, 6.99 and 7.99 fail on the broken bins (screenshot kept). [VERIFY after you run it on the old code]
- **Passes on repaired code:** yes, 7 passed.
- **Written by:** Member 2 (Neo Carl Jacinto)

### Final integrator work
- Created the `final-merge` branch from `main` and merged each member's branch into it: [LIST BRANCHES, for example origin/member1-defects-1-2, origin/fix-defect-3].
- Conflicts and how they were resolved: [DESCRIBE, or "none"].
- After merging, 2 tests still failed. Fixed in `quakewatch.py`: `split_by_contract` now uses `lazy=True`, catches `pa.errors.SchemaErrors`, and returns the good and rejected rows separately. Also fixed a typo in the `log.warning` call in `integrate()` (`and` instead of a comma) and moved the rejected-rows WARNING inside `split_by_contract`.
- Checked that the supplied tests and `tests/conftest.py` were not edited.
- Final result: `python -m pytest -q .` gave 31 passed.
- Ran `python run.py` twice: first run [NUMBERS], second run [NUMBERS] with `new_rows` equal to 0. [FILL IN]
- Created `REPAIR_LOG.md`, `pytest_output.txt`, `disclosure.txt`, and the ZIP. [TICK WHEN DONE]
