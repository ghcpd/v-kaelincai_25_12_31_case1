# Fix Summary

## Bug Description
A runtime ZeroDivisionError occurred when processing claims for policies in
`grace_period` with `grace_period_days == 0`. The error originated from
`src/claim_calculator.py` where a grace-period factor of `0` was used as a
divisor.

## Root Cause Analysis
The helper `_calculate_grace_period_factor()` returned `0` for
`grace_period_days == 0`. Later, `calculate_payout_amount()` divided the
payout by that factor, causing a `ZeroDivisionError`.

## Solution Implemented
- Ensure `_calculate_grace_period_factor()` never returns `0`.
- Treat `grace_period_days <= 0` as the conservative "maximum penalty" case
  and return a non-zero factor (business decision: `3.0`).
- Add defensive check in `calculate_payout_amount()` so any non-positive
  factor is replaced with the default maximum-penalty factor.
- Update `demo.py` to reflect the fixed behavior.

## Changes Made
- File: `src/claim_calculator.py`
  - Changed behavior for `grace_period_days <= 0` to return a non-zero
    penalty factor (maximum penalty = 3.0) instead of returning 0.
  - Added defensive guard to avoid division by zero if an unexpected
    non-positive factor is ever produced.
- File: `demo.py`
  - Updated demos so the grace-period-with-zero-days case no longer
    crashes and prints the approved amount instead.
- Other files: copied into `issue_project_fixed/` (no logic changes).

## Test Results
All tests in `issue_project_fixed/` pass.

```
pytest -q

Output:

```
14 passed in 0.15s
```
```

## Business Logic Decision
When a policy is marked `grace_period` but `grace_period_days <= 0`, the
system applies the maximum penalty factor (3.0). Rationale:
- Conservative: reduces payout rather than overpaying.
- Predictable: avoids throwing an exception for an edge case.
- Backwards-compatible: existing passing tests and behavior for
  positive grace periods are preserved.

## Verification
- [x] All 14 tests pass
- [x] `demo.py` runs without errors
- [x] No regression in existing functionality
- [x] Code follows existing style and patterns

## Notes / Follow-ups
- Consider logging or monitoring alerts when a policy is in
  `grace_period` with non-positive days — this may indicate data
  integrity issues upstream.
- If business prefers rejecting such claims instead of applying a
  maximum penalty, replace the fallback behavior with an explicit
  validation error and update tests accordingly.
