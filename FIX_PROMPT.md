# Bug Fix Task - Insurance Claim Processing System

## Task Overview

You are given an insurance claim processing system with a critical runtime bug. Your task is to analyze the failing tests, identify the root cause, fix the bug, and create a corrected version of the project in a new directory.

## Current Project Structure

```
issue_project/
├── src/
│   ├── __init__.py
│   ├── models.py                 # Data models (Policy, Claim)
│   ├── claim_calculator.py       # Core calculation logic - CONTAINS BUG
│   ├── claim_service.py          # Business service layer
│   └── claim_controller.py       # API controller simulation
│
├── tests/
│   ├── __init__.py
│   ├── test_claim_calculator.py  # Unit tests (1 failing)
│   └── test_claim_service.py     # Integration tests (1 failing)
│
├── data/
│   └── sample_claims.json        # Sample test data
│
├── demo.py                       # Bug demonstration script
├── requirements.txt              # Dependencies
├── README.md                     # Documentation
├── KNOWN_ISSUE.md               # Bug analysis (contains hints)
├── QUICKSTART.md                # Quick reference
└── PROJECT_SUMMARY.md           # Project overview
```

## Current Test Results

```
======================== short test summary info =========================
FAILED tests/test_claim_calculator.py::TestClaimCalculator::test_grace_period_with_zero_days_should_fail
FAILED tests/test_claim_service.py::TestClaimServiceIntegration::test_grace_period_claim_with_zero_days_integration_failure
======================= 2 failed, 12 passed in 0.23s =====================
```

**Error Type**: `ZeroDivisionError: float division by zero`  
**Error Location**: `src/claim_calculator.py`, line 75

## Your Tasks

### 1. Analysis Phase
- Run the existing tests to observe the failures
- Run `demo.py` to see the bug in action
- Read `KNOWN_ISSUE.md` for context (but implement your own solution)
- Identify the root cause of the `ZeroDivisionError`
- Understand the business logic around grace period calculations

### 2. Fix Implementation Phase
Create a **new directory** called `issue_project_fixed/` with the following structure:

```
issue_project_fixed/
├── src/
│   ├── __init__.py
│   ├── models.py                 # Copy from original (if no changes needed)
│   ├── claim_calculator.py       # FIXED VERSION
│   ├── claim_service.py          # Copy from original (if no changes needed)
│   └── claim_controller.py       # Copy from original (if no changes needed)
│
├── tests/
│   ├── __init__.py
│   ├── test_claim_calculator.py  # Updated tests (all should pass)
│   └── test_claim_service.py     # Updated tests (all should pass)
│
├── data/
│   └── sample_claims.json        # Copy from original
│
├── demo.py                       # Updated demo (should run without crashes)
├── requirements.txt              # Same dependencies
├── README.md                     # Updated documentation
├── FIX_SUMMARY.md               # YOUR FIX DOCUMENTATION (see below)
└── QUICKSTART.md                # Updated quick reference
```

### 3. Fix Requirements

Your fix must:
- ✅ Resolve the `ZeroDivisionError` when `grace_period_days = 0`
- ✅ Handle the edge case gracefully with sensible business logic
- ✅ Make all 14 tests pass
- ✅ Maintain backward compatibility with existing tests
- ✅ Not break any currently passing functionality
- ✅ Follow Python best practices and maintain code quality

### 4. Documentation Requirements

Create `issue_project_fixed/FIX_SUMMARY.md` with the following sections:

```markdown
# Fix Summary

## Bug Description
[Describe what the bug was]

## Root Cause Analysis
[Explain why the bug occurred]

## Solution Implemented
[Describe your fix approach without showing code]

## Changes Made
- File: [filename]
  - Line [X]: [description of change]
  - Line [Y]: [description of change]

## Test Results
[Show pytest output with all tests passing]

## Business Logic Decision
[Explain how you decided to handle grace_period_days = 0]

## Verification
- [ ] All 14 tests pass
- [ ] demo.py runs without errors
- [ ] No regression in existing functionality
- [ ] Code follows existing style and patterns
```

## Constraints

- **DO NOT** modify files in the original `issue_project/` directory
- **DO** create all files in the new `issue_project_fixed/` directory
- **DO NOT** use absolute paths in any configuration or code
- **DO** preserve the original project structure
- **DO** maintain all existing functionality that works correctly
- **DO** add comments explaining your fix in the code

## Success Criteria

Your fix is complete when:
1. ✅ Running `pytest -v` in `issue_project_fixed/` shows **14 passed, 0 failed**
2. ✅ Running `python demo.py` in `issue_project_fixed/` executes without exceptions
3. ✅ `FIX_SUMMARY.md` clearly documents your changes
4. ✅ All original passing tests still pass
5. ✅ The two previously failing tests now pass

## Getting Started

1. Navigate to the `issue_project/` directory
2. Run `pytest -v` to see the failing tests
3. Run `python demo.py` to observe the bug
4. Read `KNOWN_ISSUE.md` for context
5. Analyze the code in `src/claim_calculator.py`
6. Create your fixed version in `issue_project_fixed/`

## Hints

- The bug is in a specific calculation method
- Consider what should happen when a divisor could be zero
- The fix might involve returning a sensible default value
- Consider edge cases in your solution
- Test your fix thoroughly before considering it complete

---

**Note**: This is a learning exercise. Focus on understanding the bug, implementing a clean fix, and documenting your reasoning. Good luck!
