"""
Claim calculation utilities with INTENTIONAL BUG for demonstration
"""
from src.models import Policy, Claim


class ClaimCalculator:
    """
    Calculate claim payout amounts based on complex business rules
    
    BUG: Division by zero when grace_period_factor is 0
    """
    
    def __init__(self):
        # Business rule: Maximum claims per policy type
        self.max_claims_per_type = {
            'health': 5,
            'auto': 3,
            'home': 4,
            'life': 1
        }
        
        # Business rule: Claim count penalty rates
        self.claim_count_penalty = {
            0: 1.0,
            1: 0.95,
            2: 0.90,
            3: 0.85,
            4: 0.80,
            5: 0.75
        }
    
    def calculate_payout_amount(self, policy: Policy, claim: Claim) -> float:
        """
        Calculate the approved payout amount for a claim
        
        Formula includes multiple factors:
        - Deductible
        - Base payout rate
        - Claim count penalty
        - Grace period adjustment (CONTAINS BUG)
        - Remaining coverage check
        
        Args:
            policy: The insurance policy
            claim: The claim request
            
        Returns:
            Calculated payout amount
            
        Raises:
            ZeroDivisionError: When grace_period_factor is 0 (BUG)
            ValueError: When claim amount is invalid
        """
        if claim.claim_amount <= 0:
            raise ValueError("Claim amount must be positive")
        
        # Step 1: Apply deductible
        amount_after_deductible = max(0, claim.claim_amount - policy.deductible)
        
        if amount_after_deductible == 0:
            return 0.0
        
        # Step 2: Apply base payout rate
        base_payout = amount_after_deductible * policy.payout_rate
        
        # Step 3: Apply claim count penalty
        penalty_rate = self._get_claim_count_penalty(policy.claim_count)
        payout_with_penalty = base_payout * penalty_rate
        
        # Step 4: Apply grace period adjustment (BUG HERE!)
        if policy.is_in_grace_period():
            grace_period_factor = self._calculate_grace_period_factor(policy)
            # BUG: When grace_period_days is 0, this causes division by zero
            payout_with_penalty = payout_with_penalty / grace_period_factor
        
        # Step 5: Check against remaining coverage
        remaining_coverage = policy.get_remaining_coverage()
        final_payout = min(payout_with_penalty, remaining_coverage)
        
        return round(final_payout, 2)
    
    def _get_claim_count_penalty(self, claim_count: int) -> float:
        """Get penalty rate based on claim count"""
        if claim_count >= 5:
            return self.claim_count_penalty[5]
        return self.claim_count_penalty.get(claim_count, 0.75)
    
    def _calculate_grace_period_factor(self, policy: Policy) -> float:
        """
        Calculate grace period factor
        
        BUG: Returns 0 when grace_period_days is 0, causing division by zero
        
        Business logic intention:
        - Grace period 30 days: factor = 1.5 (reduce payout by 50%)
        - Grace period 15 days: factor = 2.0 (reduce payout by 100%)
        - Grace period 0 days: SHOULD handle this case but doesn't!
        """
        if policy.grace_period_days >= 30:
            return 1.5
        elif policy.grace_period_days >= 15:
            return 2.0
        elif policy.grace_period_days > 0:
            return 2.5
        else:
            # BUG: Returns 0, which will cause division by zero
            # Should return a default value like 3.0 or raise an exception
            return 0
    
    def validate_claim_eligibility(self, policy: Policy, claim: Claim) -> tuple[bool, str]:
        """
        Validate if a claim is eligible for processing
        
        Returns:
            Tuple of (is_eligible, reason)
        """
        # Check policy status
        if policy.status == 'lapsed':
            return False, "Policy has lapsed"
        
        if policy.status == 'cancelled':
            return False, "Policy is cancelled"
        
        # Check claim count limit
        max_claims = self.max_claims_per_type.get(policy.policy_type, 3)
        if policy.claim_count >= max_claims:
            return False, f"Exceeded maximum claims ({max_claims}) for {policy.policy_type} policy"
        
        # Check remaining coverage
        if policy.get_remaining_coverage() <= 0:
            return False, "No remaining coverage available"
        
        # Check claim amount
        if claim.claim_amount <= 0:
            return False, "Invalid claim amount"
        
        return True, "Eligible"
