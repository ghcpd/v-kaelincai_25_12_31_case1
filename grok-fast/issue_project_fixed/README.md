# Insurance Claim Processing System - FIXED

A minimal Python project demonstrating the **fix** for a Runtime Exception Bug in insurance claim processing.

## Project Overview

This system simulates an insurance claim auto-processing service with complex business rules including:
- Multiple policy types (health, auto, home, life)
- Deductible calculations
- Claim count penalties
- Grace period adjustments
- Coverage limit validations

## Bug Fix Summary

**Original Bug**: `ZeroDivisionError` - Runtime Exception

**Location**: `src/claim_calculator.py`, line 75

**Trigger Condition**: When a policy has status `grace_period` with `grace_period_days = 0`

**Fix Applied**: Changed `_calculate_grace_period_factor()` to return `3.0` instead of `0` when `grace_period_days <= 0`

**Result**: System now handles edge case gracefully with maximum penalty factor

## Project Structure

```
issue_project_fixed/
├── src/
│   ├── __init__.py
│   ├── models.py              # Policy and Claim data models
│   ├── claim_calculator.py    # Core calculation logic (FIXED)
│   ├── claim_service.py       # Business service layer
│   └── claim_controller.py    # API controller simulation
├── tests/
│   ├── __init__.py
│   ├── test_claim_calculator.py    # Unit tests (all passing)
│   └── test_claim_service.py       # Integration tests (all passing)
├── data/
│   └── sample_claims.json     # Sample test data
├── requirements.txt           # Python dependencies
├── README.md                 # This file
├── FIX_SUMMARY.md            # Detailed fix documentation
└── QUICKSTART.md             # Quick reference
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip

### Install Dependencies

```powershell
pip install -r requirements.txt
```

## Running Tests

### Run all tests (all should pass)
```powershell
pytest -v
```

### Run with coverage report
```powershell
pytest --cov=src --cov-report=term-missing
```

### Run specific test file
```powershell
pytest tests/test_claim_calculator.py -v
pytest tests/test_claim_service.py -v
```

### Expected Test Results

- **Total tests**: 14
- **Passing tests**: 14
- **Failing tests**: 0

All tests now pass, confirming the bug has been fixed.

## Quick Start Example

```python
from src.models import Policy, Claim
from src.claim_calculator import ClaimCalculator

# Create a normal policy
policy = Policy(
    policy_id="P001",
    policy_type="auto",
    status="active",
    deductible=500.0,
    coverage_limit=20000.0,
    payout_rate=0.85
)

# Create a claim
claim = Claim(
    claim_id="C001",
    policy_id="P001",
    claim_amount=3000.0,
    claim_type="collision",
    description="Minor accident"
)

# Calculate payout (works fine)
calculator = ClaimCalculator()
payout = calculator.calculate_payout_amount(policy, claim)
print(f"Approved amount: ${payout}")  # Output: Approved amount: $2125.0
```

### Grace Period with 0 Days (Now Works!)

```python
# Create policy in grace period with 0 days (FIXED!)
fixed_policy = Policy(
    policy_id="P002",
    policy_type="home",
    status="grace_period",
    deductible=1000.0,
    coverage_limit=50000.0,
    payout_rate=0.9,
    grace_period_days=0  # Now works with maximum penalty!
)

claim = Claim(
    claim_id="C002",
    policy_id="P002",
    claim_amount=5000.0,
    claim_type="water_damage",
    description="Basement flooding"
)

# This now works correctly with maximum penalty factor (3.0)
calculator.calculate_payout_amount(fixed_policy, claim)
# Output: 1020.0 (with maximum penalty applied)
```

## Test Data

Sample claims are provided in `data/sample_claims.json`:
- **SAMPLE_001**: Now works (grace period with 0 days)
- **SAMPLE_002**: Normal claim (works correctly)
- **SAMPLE_003**: Grace period with 30 days (works correctly)

## Key Files

### Fix Location
- **File**: [src/claim_calculator.py](src/claim_calculator.py#L108)
- **Method**: `_calculate_grace_period_factor()`
- **Fix**: Return `3.0` instead of `0` for maximum penalty

### Updated Tests
- [tests/test_claim_calculator.py](tests/test_claim_calculator.py#L64-L96) - Unit test (now passes)
- [tests/test_claim_service.py](tests/test_claim_service.py#L95-L123) - Integration test (now passes)

## Business Logic Context

The system uses complex business rules:

1. **Deductible**: Amount subtracted from claim before calculation
2. **Payout Rate**: Base percentage of coverage (e.g., 80%, 90%)
3. **Claim Count Penalty**: Reduces payout based on previous claims
   - 0 claims: 100%
   - 1 claim: 95%
   - 2 claims: 90%
   - etc.
4. **Grace Period Factor**: Additional reduction for policies in grace period
   - 30+ days: 1.5x reduction
   - 15-29 days: 2.0x reduction
   - 1-14 days: 2.5x reduction
   - **0 days: 3.0x reduction (FIXED!)**

## Next Steps

See [FIX_SUMMARY.md](FIX_SUMMARY.md) for detailed fix documentation.