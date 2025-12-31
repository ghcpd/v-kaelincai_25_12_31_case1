"""
API Controller layer (simulated)
"""
from typing import Dict, Any
from src.claim_service import ClaimService


class ClaimController:
    """Controller for handling claim API requests"""
    
    def __init__(self):
        self.claim_service = ClaimService()
    
    def submit_claim(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle POST /api/claims/submit
        
        This simulates the API endpoint that returns 500 error
        
        Returns:
            API response with status code and data
        """
        try:
            result = self.claim_service.submit_claim(request_data)
            return {
                'status_code': 200,
                'data': result
            }
        except ZeroDivisionError as e:
            # BUG: This exception is not caught in the real scenario
            # Causes 500 Internal Server Error
            return {
                'status_code': 500,
                'error': 'Internal Server Error',
                'message': 'An unexpected error occurred during claim processing'
            }
        except ValueError as e:
            return {
                'status_code': 404,
                'error': 'Not Found',
                'message': str(e)
            }
        except Exception as e:
            return {
                'status_code': 500,
                'error': 'Internal Server Error',
                'message': 'An unexpected error occurred'
            }