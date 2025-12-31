# Fix Summary

## Bug Description
The application crashed with a `ZeroDivisionError` when processing claims for
policies in `grace_period` that had `grace_period_days == 0`.

## Root Cause Analysis
The helper `_calculate_grace_period_factor()` returned `0` when
`grace_period_days == 0`. `calculate_payout_amount()` divided the payout by
that factor, causing a division-by-zero runtime error.

## Solution Implemented
- Return a sensible, non-zero factor for `grace_period_days == 0` (maximum
  penalty factor = `3.0`).
- Add a defensive check in `calculate_payout_amount()` so a non-positive
  grace factor is replaced by the maximum penalty.
- No behavioral changes for existing valid inputs; only the 0-day edge case
  is handled.

## Changes Made
- File: `src/claim_calculator.py`
  - Fixed `_calculate_grace_period_factor()` to return `3.0` for `0` days
  - Added defensive handling in `calculate_payout_amount()` to avoid
    division by zero when factor is non-positive

- Files copied into `issue_project_fixed/` (no functional changes):
  - `src/models.py`, `src/claim_service.py`, `src/claim_controller.py`, `src/__init__.py`
  - `tests/test_claim_calculator.py`, `tests/test_claim_service.py`
  - `data/sample_claims.json`, `demo.py`, `README.md`, `QUICKSTART.md`, `requirements.txt`

## Test Results
All tests in the fixed project pass.

```
14 passed in 0.05s
```

## Business Logic Decision
When `grace_period_days == 0` we treat the policy as having the *maximum*
penalty (factor = 3.0). Rationale:
- Returning 0 caused a crash — unacceptable in production.
- Using a high penalty ensures claimants still receive a result (reduced
  payout) rather than an exception.
- This preserves backward compatibility for valid grace period values.

## Verification
- [x] All 14 tests pass
- [x] `demo.py` runs without errors
- [x] No regression in existing functionality
- [x] Code follows existing style and patterns

---

If you want, I can open a follow-up PR with a small changelog and add an
explicit unit test asserting the exact payout for the 0-day case (currently
we assert payout > 0).