"""
Integration tests for ClaimService - These tests WILL FAIL due to the bug
"""
import pytest
from datetime import datetime
from src.models import Policy, Claim
from src.claim_service import ClaimService


class TestClaimServiceIntegration:
    """Integration tests for claim processing workflow"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.service = ClaimService()
    
    def test_successful_claim_processing(self):
        """Test end-to-end claim processing for normal case"""
        # Setup policy
        policy = Policy(
            policy_id="P101",
            policy_type="auto",
            status="active",
            deductible=500.0,
            coverage_limit=20000.0,
            payout_rate=0.85,
            claim_count=0,
            total_claimed=0.0
        )
        self.service.add_policy(policy)
        
        # Submit claim
        claim_data = {
            'claim_id': 'C101',
            'policy_id': 'P101',
            'claim_amount': 3000.0,
            'claim_type': 'collision',
            'description': 'Minor fender bender'
        }
        
        result = self.service.submit_claim(claim_data)
        
        assert result['status'] == 'approved'
        assert result['approved_amount'] == 2125.0  # (3000-500) * 0.85 * 1.0
        assert result['claim_id'] == 'C101'
        
        # Verify policy updated
        updated_policy = self.service.get_policy('P101')
        assert updated_policy.claim_count == 1
        assert updated_policy.total_claimed == 2125.0
    
    def test_claim_rejection_for_lapsed_policy(self):
        """Test claim rejection when policy is lapsed"""
        policy = Policy(
            policy_id="P102",
            policy_type="health",
            status="lapsed",
            deductible=300.0,
            coverage_limit=10000.0,
            payout_rate=0.8,
            claim_count=2,
            total_claimed=3000.0
        )
        self.service.add_policy(policy)
        
        claim_data = {
            'claim_id': 'C102',
            'policy_id': 'P102',
            'claim_amount': 2000.0,
            'claim_type': 'medical',
            'description': 'Hospital stay'
        }
        
        result = self.service.submit_claim(claim_data)
        
        assert result['status'] == 'rejected'
        assert result['reason'] == 'Policy has lapsed'
        assert result['approved_amount'] == 0.0
    
    def test_grace_period_claim_with_zero_days_maximum_penalty(self):
        """
        Test grace period claim processing with 0 days - applies maximum penalty
        
        When a policy is in grace_period with 0 days, the system processes
        the claim with maximum penalty factor (3.0) to discourage late claims.
        
        Expected: Claim approved with reduced payout amount due to maximum penalty
        """
        # Setup policy in grace period with 0 days
        policy = Policy(
            policy_id="P103",
            policy_type="home",
            status="grace_period",
            deductible=1500.0,
            coverage_limit=75000.0,
            payout_rate=0.9,
            claim_count=1,
            total_claimed=10000.0,
            grace_period_days=0  # 0 days remaining in grace period
        )
        self.service.add_policy(policy)
        
        claim_data = {
            'claim_id': 'C103',
            'policy_id': 'P103',
            'claim_amount': 8000.0,
            'claim_type': 'water_damage',
            'description': 'Basement flooding'
        }
        
        # Expected: (8000 - 1500) * 0.9 * 0.95 / 3.0 = 6500 * 0.9 * 0.95 / 3.0 = 5850 * 0.95 / 3.0 = 5557.5 / 3.0 = 1852.5
        result = self.service.submit_claim(claim_data)
        assert result['status'] == 'approved'
        assert result['approved_amount'] == 1852.5
        assert 'claim_id' in result
    
    def test_grace_period_with_valid_days(self):
        """Test grace period processing with valid grace period days"""
        policy = Policy(
            policy_id="P104",
            policy_type="health",
            status="grace_period",
            deductible=400.0,
            coverage_limit=12000.0,
            payout_rate=0.85,
            claim_count=0,
            total_claimed=0.0,
            grace_period_days=25  # Valid grace period
        )
        self.service.add_policy(policy)
        
        claim_data = {
            'claim_id': 'C104',
            'policy_id': 'P104',
            'claim_amount': 2500.0,
            'claim_type': 'medical',
            'description': 'Surgery'
        }
        
        result = self.service.submit_claim(claim_data)
        
        # Expected: (2500 - 400) * 0.85 * 1.0 / 2.0 = 892.5
        assert result['status'] == 'approved'
        assert result['approved_amount'] == 892.5
    
    def test_multiple_claims_penalty_progression(self):
        """Test that claim count penalties apply correctly"""
        policy = Policy(
            policy_id="P105",
            policy_type="auto",
            status="active",
            deductible=200.0,
            coverage_limit=15000.0,
            payout_rate=0.9,
            claim_count=0,
            total_claimed=0.0
        )
        self.service.add_policy(policy)
        
        # First claim - no penalty
        claim_data_1 = {
            'claim_id': 'C105_1',
            'policy_id': 'P105',
            'claim_amount': 1000.0,
            'claim_type': 'collision',
            'description': 'First claim'
        }
        result1 = self.service.submit_claim(claim_data_1)
        assert result1['approved_amount'] == 720.0  # (1000-200) * 0.9 * 1.0
        
        # Second claim - 5% penalty
        claim_data_2 = {
            'claim_id': 'C105_2',
            'policy_id': 'P105',
            'claim_amount': 1000.0,
            'claim_type': 'collision',
            'description': 'Second claim'
        }
        result2 = self.service.submit_claim(claim_data_2)
        assert result2['approved_amount'] == 684.0  # (1000-200) * 0.9 * 0.95
    
    def test_policy_not_found(self):
        """Test error handling when policy doesn't exist"""
        claim_data = {
            'claim_id': 'C999',
            'policy_id': 'P999',
            'claim_amount': 1000.0,
            'claim_type': 'unknown',
            'description': 'Test claim'
        }
        
        with pytest.raises(ValueError, match="Policy P999 not found"):
            self.service.submit_claim(claim_data)