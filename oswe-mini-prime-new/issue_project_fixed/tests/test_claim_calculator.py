"""
Unit tests for ClaimCalculator
"""
import pytest
from datetime import datetime, timedelta
from src.models import Policy, Claim
from src.claim_calculator import ClaimCalculator


class TestClaimCalculator:
    """Test suite for ClaimCalculator"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.calculator = ClaimCalculator()
    
    def test_normal_claim_calculation(self):
        """Test normal claim calculation for active policy"""
        policy = Policy(
            policy_id="P001",
            policy_type="health",
            status="active",
            deductible=500.0,
            coverage_limit=10000.0,
            payout_rate=0.8,
            claim_count=1,
            total_claimed=2000.0
        )
        
        claim = Claim(
            claim_id="C001",
            policy_id="P001",
            claim_amount=3000.0,
            claim_type="medical",
            description="Hospital visit"
        )
        
        # Expected: (3000 - 500) * 0.8 * 0.95 = 1900
        payout = self.calculator.calculate_payout_amount(policy, claim)
        assert payout == 1900.0
    
    def test_grace_period_with_30_days(self):
        """Test calculation for policy in grace period with 30 days"""
        policy = Policy(
            policy_id="P002",
            policy_type="auto",
            status="grace_period",
            deductible=300.0,
            coverage_limit=15000.0,
            payout_rate=0.9,
            claim_count=0,
            total_claimed=0.0,
            grace_period_days=30
        )
        
        claim = Claim(
            claim_id="C002",
            policy_id="P002",
            claim_amount=2000.0,
            claim_type="collision",
            description="Car accident"
        )
        
        # Expected: (2000 - 300) * 0.9 * 1.0 / 1.5 = 1020
        payout = self.calculator.calculate_payout_amount(policy, claim)
        assert payout == 1020.0
    
    def test_grace_period_with_zero_days_should_fail(self):
        """
        TEST FAILURE: This test demonstrates the bug
        """
        policy = Policy(
            policy_id="P003",
            policy_type="home",
            status="grace_period",
            deductible=1000.0,
            coverage_limit=50000.0,
            payout_rate=0.85,
            claim_count=2,
            total_claimed=5000.0,
            grace_period_days=0
        )
        
        claim = Claim(
            claim_id="C003",
            policy_id="P003",
            claim_amount=5000.0,
            claim_type="fire_damage",
            description="Kitchen fire damage"
        )
        
        payout = self.calculator.calculate_payout_amount(policy, claim)
        assert payout > 0
        assert isinstance(payout, float)
    
    def test_grace_period_boundary_case_15_days(self):
        """Test grace period with 15 days (boundary case)"""
        policy = Policy(
            policy_id="P004",
            policy_type="health",
            status="grace_period",
            deductible=200.0,
            coverage_limit=8000.0,
            payout_rate=0.8,
            claim_count=0,
            total_claimed=0.0,
            grace_period_days=15
        )
        
        claim = Claim(
            claim_id="C004",
            policy_id="P004",
            claim_amount=1500.0,
            claim_type="medical",
            description="Medical checkup"
        )
        
        # Expected: (1500 - 200) * 0.8 * 1.0 / 2.0 = 520
        payout = self.calculator.calculate_payout_amount(policy, claim)
        assert payout == 520.0
    
    def test_claim_exceeds_remaining_coverage(self):
        """Test claim that exceeds remaining coverage"""
        policy = Policy(
            policy_id="P005",
            policy_type="auto",
            status="active",
            deductible=500.0,
            coverage_limit=10000.0,
            payout_rate=0.9,
            claim_count=1,
            total_claimed=9000.0  # Only 1000 remaining
        )
        
        claim = Claim(
            claim_id="C005",
            policy_id="P005",
            claim_amount=5000.0,
            claim_type="collision",
            description="Major accident"
        )
        
        # Expected: Min((5000 - 500) * 0.9 * 0.95, 1000) = 1000
        payout = self.calculator.calculate_payout_amount(policy, claim)
        assert payout == 1000.0
    
    def test_claim_amount_below_deductible(self):
        """Test claim amount less than deductible"""
        policy = Policy(
            policy_id="P006",
            policy_type="health",
            status="active",
            deductible=1000.0,
            coverage_limit=15000.0,
            payout_rate=0.8,
            claim_count=0,
            total_claimed=0.0
        )
        
        claim = Claim(
            claim_id="C006",
            policy_id="P006",
            claim_amount=800.0,
            claim_type="medical",
            description="Minor treatment"
        )
        
        # Expected: 0 (claim less than deductible)
        payout = self.calculator.calculate_payout_amount(policy, claim)
        assert payout == 0.0
    
    def test_validate_claim_eligibility_lapsed_policy(self):
        """Test claim validation for lapsed policy"""
        policy = Policy(
            policy_id="P007",
            policy_type="life",
            status="lapsed",
            deductible=0.0,
            coverage_limit=100000.0,
            payout_rate=1.0
        )
        
        claim = Claim(
            claim_id="C007",
            policy_id="P007",
            claim_amount=50000.0,
            claim_type="death",
            description="Life claim"
        )
        
        is_eligible, reason = self.calculator.validate_claim_eligibility(policy, claim)
        assert is_eligible is False
        assert reason == "Policy has lapsed"
    
    def test_validate_claim_eligibility_exceeded_max_claims(self):
        """Test claim validation when max claims exceeded"""
        policy = Policy(
            policy_id="P008",
            policy_type="health",
            status="active",
            deductible=500.0,
            coverage_limit=10000.0,
            payout_rate=0.8,
            claim_count=5  # Max is 5 for health
        )
        
        claim = Claim(
            claim_id="C008",
            policy_id="P008",
            claim_amount=1000.0,
            claim_type="medical",
            description="Another medical claim"
        )
        
        is_eligible, reason = self.calculator.validate_claim_eligibility(policy, claim)
        assert is_eligible is False
        assert "Exceeded maximum claims" in reason
