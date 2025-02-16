"""
This module contains pure functions for book validation.
Functions are used because these operations:
1. Don't need to maintain state
2. Always return the same output for the same input
3. Have no side effects
"""

def is_valid_isbn(isbn: str) -> bool:
    """
    Validates ISBN format (simplified for example).
    Pure function: same input always yields same output.
    """
    # Remove hyphens and spaces
    isbn = isbn.replace("-", "").replace(" ", "")
    
    if len(isbn) not in (10, 13):
        return False
        
    # Check if all characters are digits (simplified validation)
    return isbn.isdigit()

def is_valid_title(title: str) -> bool:
    """
    Validates book title.
    Pure function with no side effects.
    """
    return bool(title.strip()) and len(title) <= 200

def calculate_late_fee(days_overdue: int) -> float:
    """
    Calculates late fee based on days overdue.
    Pure function: mathematical calculation with no side effects.
    """
    BASE_FEE = 0.50  # 50 cents per day
    MAX_FEE = 20.00
    
    fee = days_overdue * BASE_FEE
    return min(fee, MAX_FEE) 