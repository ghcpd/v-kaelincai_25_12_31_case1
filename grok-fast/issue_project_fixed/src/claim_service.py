"""
Business service layer for claim processing
"""
from typing import Dict, Any
from src.models import Policy, Claim
from src.claim_calculator import ClaimCalculator


class ClaimService:
    """Service for processing insurance claims"""
    
    def __init__(self):
        self.calculator = ClaimCalculator()
        # In-memory storage (simulating database)
        self.policies: Dict[str, Policy] = {}
        self.claims: Dict[str, Claim] = {}
    
    def add_policy(self, policy: Policy) -> None:
        """Add a policy to the system"""
        self.policies[policy.policy_id] = policy
    
    def get_policy(self, policy_id: str) -> Policy:
        """Retrieve a policy by ID"""
        if policy_id not in self.policies:
            raise ValueError(f"Policy {policy_id} not found")
        return self.policies[policy_id]
    
    def process_auto_claim(self, claim: Claim) -> Dict[str, Any]:
        """
        Automatically process a claim request
        
        This is the main entry point that triggers the bug
        
        Returns:
            Dictionary with processing result
            
        Raises:
            ZeroDivisionError: When policy is in grace period with 0 days (BUG)
        """
        # Get associated policy
        policy = self.get_policy(claim.policy_id)
        
        # Validate eligibility
        is_eligible, reason = self.calculator.validate_claim_eligibility(policy, claim)
        
        if not is_eligible:
            claim.status = 'rejected'
            claim.rejection_reason = reason
            self.claims[claim.claim_id] = claim
            return {
                'status': 'rejected',
                'claim_id': claim.claim_id,
                'reason': reason,
                'approved_amount': 0.0
            }
        
        # Calculate payout (BUG OCCURS HERE for grace period with 0 days)
        try:
            approved_amount = self.calculator.calculate_payout_amount(policy, claim)
            
            # Update claim
            claim.status = 'approved'
            claim.approved_amount = approved_amount
            self.claims[claim.claim_id] = claim
            
            # Update policy
            policy.claim_count += 1
            policy.total_claimed += approved_amount
            
            return {
                'status': 'approved',
                'claim_id': claim.claim_id,
                'approved_amount': approved_amount,
                'remaining_coverage': policy.get_remaining_coverage()
            }
        except ZeroDivisionError:
            # In production, this exception is NOT caught, causing 500 error
            # Re-raise to simulate the bug
            raise
    
    def submit_claim(self, claim_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Submit a new claim (simulates API endpoint)
        
        Args:
            claim_data: Dictionary with claim information
            
        Returns:
            Processing result
        """
        claim = Claim(
            claim_id=claim_data['claim_id'],
            policy_id=claim_data['policy_id'],
            claim_amount=claim_data['claim_amount'],
            claim_type=claim_data['claim_type'],
            description=claim_data['description']
        )
        
        return self.process_auto_claim(claim)