# Insurance Claim Processing System

A minimal Python project demonstrating a **Runtime Exception Bug** in insurance claim processing.

## Project Overview

This system simulates an insurance claim auto-processing service with complex business rules including:
- Multiple policy types (health, auto, home, life)
- Deductible calculations
- Claim count penalties
- Grace period adjustments
- Coverage limit validations

## Bug Description

**Type**: `ZeroDivisionError` - Runtime Exception

**Location**: `src/claim_calculator.py`, line 67

**Trigger Condition**: When a policy has status `grace_period` with `grace_period_days = 0`

**Expected Behavior**: System should handle edge case gracefully (either use default factor or reject claim)

**Actual Behavior**: Division by zero exception crashes the API, returning HTTP 500

**Impact**: All users with policies in grace period (day 0) cannot submit claims

## Project Structure

```
issue_project/
├── src/
│   ├── __init__.py
│   ├── models.py              # Policy and Claim data models
│   ├── claim_calculator.py    # Core calculation logic (CONTAINS BUG)
│   ├── claim_service.py       # Business service layer
│   └── claim_controller.py    # API controller simulation
├── tests/
│   ├── __init__.py
│   ├── test_claim_calculator.py    # Unit tests (2 failing tests)
│   └── test_claim_service.py       # Integration tests (1 failing test)
├── data/
│   └── sample_claims.json     # Sample test data
├── requirements.txt           # Python dependencies
├── README.md                 # This file
└── KNOWN_ISSUE.md            # Detailed bug analysis
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

### Run all tests (will show failures)
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
- **Passing tests**: 12
- **Failing tests**: 2
  - `test_grace_period_with_zero_days_should_fail` (unit test) - ZeroDivisionError
  - `test_grace_period_claim_with_zero_days_integration_failure` (integration test) - ZeroDivisionError

The failing tests clearly demonstrate the bug exists and needs to be fixed.

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

### Triggering the Bug

```python
# Create policy in grace period with 0 days (BUG!)
buggy_policy = Policy(
    policy_id="P002",
    policy_type="home",
    status="grace_period",
    deductible=1000.0,
    coverage_limit=50000.0,
    payout_rate=0.9,
    grace_period_days=0  # This triggers the bug!
)

claim = Claim(
    claim_id="C002",
    policy_id="P002",
    claim_amount=5000.0,
    claim_type="water_damage",
    description="Basement flooding"
)

# This will crash with ZeroDivisionError
calculator.calculate_payout_amount(buggy_policy, claim)
```

## Test Data

Sample claims are provided in `data/sample_claims.json`:
- **SAMPLE_001**: Triggers the bug (grace period with 0 days)
- **SAMPLE_002**: Normal claim (works correctly)
- **SAMPLE_003**: Grace period with 30 days (works correctly)

## Key Files

### Bug Location
- **File**: [src/claim_calculator.py](src/claim_calculator.py#L67)
- **Method**: `calculate_payout_amount()`
- **Root Cause**: `_calculate_grace_period_factor()` returns 0 when `grace_period_days == 0`

### Failing Tests
- [tests/test_claim_calculator.py](tests/test_claim_calculator.py#L64-L96) - Unit test
- [tests/test_claim_service.py](tests/test_claim_service.py#L95-L123) - Integration test

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
   - **0 days: Returns 0 (BUG!)**

## Next Steps

See [KNOWN_ISSUE.md](KNOWN_ISSUE.md) for detailed analysis and fix suggestions.
