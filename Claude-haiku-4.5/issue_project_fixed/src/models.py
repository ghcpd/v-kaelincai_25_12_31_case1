"""
Data models for insurance claim system
"""
from datetime import datetime, timedelta
from typing import Optional


class Policy:
    """Represents an insurance policy"""
    
    POLICY_TYPES = ['health', 'auto', 'home', 'life']
    POLICY_STATUSES = ['active', 'grace_period', 'lapsed', 'cancelled']
    
    def __init__(
        self,
        policy_id: str,
        policy_type: str,
        status: str,
        deductible: float,
        coverage_limit: float,
        payout_rate: float,
        claim_count: int = 0,
        total_claimed: float = 0.0,
        start_date: Optional[datetime] = None,
        grace_period_days: int = 0
    ):
        self.policy_id = policy_id
        self.policy_type = policy_type
        self.status = status
        self.deductible = deductible
        self.coverage_limit = coverage_limit
        self.payout_rate = payout_rate
        self.claim_count = claim_count
        self.total_claimed = total_claimed
        self.start_date = start_date or datetime.now()
        self.grace_period_days = grace_period_days
    
    def get_remaining_coverage(self) -> float:
        """Calculate remaining coverage amount"""
        return self.coverage_limit - self.total_claimed
    
    def get_days_remaining(self) -> int:
        """Calculate days remaining in policy period (assume 1 year)"""
        end_date = self.start_date + timedelta(days=365)
        remaining = (end_date - datetime.now()).days
        return max(0, remaining)
    
    def is_in_grace_period(self) -> bool:
        """Check if policy is in grace period"""
        return self.status == 'grace_period'


class Claim:
    """Represents an insurance claim request"""
    
    CLAIM_STATUSES = ['pending', 'approved', 'rejected', 'processing']
    
    def __init__(
        self,
        claim_id: str,
        policy_id: str,
        claim_amount: float,
        claim_type: str,
        description: str,
        submit_date: Optional[datetime] = None
    ):
        self.claim_id = claim_id
        self.policy_id = policy_id
        self.claim_amount = claim_amount
        self.claim_type = claim_type
        self.description = description
        self.submit_date = submit_date or datetime.now()
        self.status = 'pending'
        self.approved_amount: Optional[float] = None
        self.rejection_reason: Optional[str] = None
