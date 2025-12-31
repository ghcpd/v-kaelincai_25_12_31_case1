"""
Demonstration script for the fixed project
"""
from src.models import Policy, Claim
from src.claim_calculator import ClaimCalculator
from src.claim_service import ClaimService


def demo_normal_claim():
    print("=" * 60)
    print("DEMO 1: Normal Claim Processing")
    print("=" * 60)

    policy = Policy(
        policy_id="DEMO_001",
        policy_type="auto",
        status="active",
        deductible=500.0,
        coverage_limit=20000.0,
        payout_rate=0.85,
        claim_count=0,
        total_claimed=0.0
    )

    claim = Claim(
        claim_id="CLAIM_001",
        policy_id="DEMO_001",
        claim_amount=3000.0,
        claim_type="collision",
        description="Minor fender bender"
    )

    calculator = ClaimCalculator()

    try:
        payout = calculator.calculate_payout_amount(policy, claim)
        print(f"✓ Success! Approved Amount: ${payout}")
    except Exception as e:
        print(f"✗ Error: {e}")


def demo_grace_period_30_days():
    print("=" * 60)
    print("DEMO 2: Grace Period with 30 Days")
    print("=" * 60)

    policy = Policy(
        policy_id="DEMO_002",
        policy_type="health",
        status="grace_period",
        deductible=400.0,
        coverage_limit=15000.0,
        payout_rate=0.8,
        claim_count=1,
        total_claimed=2000.0,
        grace_period_days=30
    )

    claim = Claim(
        claim_id="CLAIM_002",
        policy_id="DEMO_002",
        claim_amount=2500.0,
        claim_type="medical",
        description="Hospital visit"
    )

    calculator = ClaimCalculator()

    try:
        payout = calculator.calculate_payout_amount(policy, claim)
        print(f"✓ Success! Approved Amount: ${payout}")
    except Exception as e:
        print(f"✗ Error: {e}")


def demo_grace_period_zero_days_fixed():
    print("=" * 60)
    print("DEMO 3: Grace Period with 0 Days (FIXED)")
    print("=" * 60)

    policy = Policy(
        policy_id="DEMO_003",
        policy_type="home",
        status="grace_period",
        deductible=1000.0,
        coverage_limit=50000.0,
        payout_rate=0.9,
        claim_count=2,
        total_claimed=10000.0,
        grace_period_days=0
    )

    claim = Claim(
        claim_id="CLAIM_003",
        policy_id="DEMO_003",
        claim_amount=5000.0,
        claim_type="water_damage",
        description="Basement flooding"
    )

    calculator = ClaimCalculator()

    try:
        payout = calculator.calculate_payout_amount(policy, claim)
        print(f"✓ Success! Approved Amount: ${payout} (no crash)")
    except Exception as e:
        print(f"✗ Error: {e}")


def demo_integration_test():
    print("=" * 60)
    print("DEMO 4: Full Integration Test (API Simulation)")
    print("=" * 60)

    service = ClaimService()

    policy = Policy(
        policy_id="POL_999",
        policy_type="home",
        status="grace_period",
        deductible=1500.0,
        coverage_limit=75000.0,
        payout_rate=0.9,
        claim_count=1,
        total_claimed=8000.0,
        grace_period_days=0
    )
    service.add_policy(policy)

    claim_data = {
        'claim_id': 'CLAIM_999',
        'policy_id': 'POL_999',
        'claim_amount': 6000.0,
        'claim_type': 'fire_damage',
        'description': 'Kitchen fire'
    }

    result = service.submit_claim(claim_data)
    print(f"✓ Response: {result}")


if __name__ == "__main__":
    demo_normal_claim()
    demo_grace_period_30_days()
    demo_grace_period_zero_days_fixed()
    demo_integration_test()
