# Quick Start Guide

## Project Setup (One Command)

```powershell
# Install dependencies and run tests
pip install -r requirements.txt; pytest -v
```

## See the Bug in Action

```powershell
python demo.py
```

## Project Structure

```
issue_project/
├── src/                          # Source code
│   ├── models.py                 # Data models
│   ├── claim_calculator.py       # ⚠ Contains the bug
│   ├── claim_service.py          # Service layer
│   └── claim_controller.py       # API controller
├── tests/                        # Test suite
│   ├── test_claim_calculator.py  # Unit tests
│   └── test_claim_service.py     # Integration tests
├── data/                         # Sample data
│   └── sample_claims.json
├── demo.py                       # ⭐ Run this to see the bug
├── README.md                     # Full documentation
├── KNOWN_ISSUE.md                # Detailed bug analysis
└── requirements.txt              # Dependencies
```

## The Bug

**Location**: [src/claim_calculator.py](src/claim_calculator.py), line 75

**Trigger**: Policy with `status="grace_period"` and `grace_period_days=0`

**Error**: `ZeroDivisionError: float division by zero`

**Result**: HTTP 500 Internal Server Error

## Test Results

```
✓ 12 tests pass (normal operations)
✗ 2 tests fail with ZeroDivisionError (demonstrating the bug)
```

The failing tests clearly show the bug exists and needs to be fixed.

## Key Commands

```powershell
# Run all tests
pytest -v

# Run with coverage
pytest --cov=src --cov-report=term-missing

# See bug demonstration
python demo.py

# Run specific test
pytest tests/test_claim_calculator.py::TestClaimCalculator::test_grace_period_with_zero_days_should_fail -v
```

## Next Steps

1. Review [KNOWN_ISSUE.md](KNOWN_ISSUE.md) for fix suggestions
2. Choose a fix approach (recommended: Option 1 + 4)
3. Implement the fix
4. Verify all tests pass
5. Add regression tests

## Business Context

This simulates an insurance claim auto-processing system with:
- Multiple policy types
- Complex payout calculations
- Grace period handling
- Claim count penalties

The bug occurs in edge case when grace period expires (day 0).
