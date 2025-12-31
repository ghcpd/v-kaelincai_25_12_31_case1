"""
Claim calculation utilities - FIXED

This version fixes a division-by-zero bug when `grace_period_days == 0`.
"""
from src.models import Policy, Claim


class ClaimCalculator:
    """
    Calculate claim payout amounts based on complex business rules
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

        Safe against grace_period_days == 0 by treating that case as the
        maximum penalty (business decision: factor = 3.0).
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

        # Step 4: Apply grace period adjustment (FIXED)
        if policy.is_in_grace_period():
            grace_period_factor = self._calculate_grace_period_factor(policy)
            # Defensive: never divide by zero or negative factor
            if grace_period_factor <= 0:
                # Business decision: treat 0 or invalid factor as maximum penalty
                grace_period_factor = 3.0
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

        Business logic:
        - Grace period 30 days: factor = 1.5 (reduce payout by 50%)
        - Grace period 15 days: factor = 2.0 (reduce payout by 100%)
        - Grace period 1-14 days: factor = 2.5
        - Grace period 0 days: treat as maximum penalty factor = 3.0

        The previous implementation returned 0 for 0 days which caused a
        division-by-zero in payout calculation. We now return 3.0 instead
        and keep a defensive check in the caller.
        """
        if policy.grace_period_days >= 30:
            return 1.5
        elif policy.grace_period_days >= 15:
            return 2.0
        elif policy.grace_period_days > 0:
            return 2.5
        else:
            # Return maximum penalty factor instead of 0 to avoid division by
            # zero and to reflect the most severe reduction for expired
            # grace periods.
            return 3.0

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
