# Fix Summary

## Bug Description
The system crashed with `ZeroDivisionError` when processing claims for policies
in `grace_period` where `grace_period_days == 0`.

## Root Cause Analysis
The helper `_calculate_grace_period_factor()` returned `0` for the `0`-day
case. The returned factor was used as a divisor in `calculate_payout_amount()`,
causing a division-by-zero runtime exception.

## Solution Implemented
- Implemented a safe default for the `0`-day grace period case: return a
  *maximum penalty factor* of `3.0` instead of `0`.
- Added a defensive check in `calculate_payout_amount()` to fall back to `3.0`
  if the calculated factor is zero or negative.
- Updated `demo.py` to demonstrate the fixed behavior and updated documentation.

## Changes Made
- File: `src/claim_calculator.py`
  - Changed the `else` branch in `_calculate_grace_period_factor()` to return `3.0`.
  - Added a defensive check before dividing by `grace_period_factor` to ensure
    it is positive; if not, fallback to `3.0`.
- File: `demo.py`
  - Updated demo messages and final summary to reflect the bug is fixed.
- Other: Copied files into `issue_project_fixed/` with updated README and docs.

## Test Results
All tests pass in the fixed project:

```
$ pytest -q
..............
14 passed in 0.15s
```

## Business Logic Decision
We treat `grace_period_days == 0` as a valid boundary state and apply the
**maximum penalty factor (3.0)**. This preserves processing continuity and
avoids crashing the system. The choice keeps behavior predictable and avoids
blocking claims in transition states. If business requires rejecting claims on
day 0, the code can be adapted to reject explicitly.

## Verification
- [x] All 14 tests pass
- [x] `demo.py` runs without errors
- [x] No regression in existing functionality
- [x] Code follows existing style and patterns
