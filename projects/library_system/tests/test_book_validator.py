import pytest
from src.services.book_validator import is_valid_isbn, is_valid_title, calculate_late_fee

@pytest.mark.parametrize("isbn,expected", [
    ("1234567890", True),      # 10 digits
    ("1234567890123", True),   # 13 digits
    ("123456789", False),      # Too short
    ("12345678901234", False), # Too long
    ("123-456-789-0", True),   # With hyphens
    ("123 456 7890", True),    # With spaces
    ("123abc4567", False),     # With letters
])
def test_isbn_validation(isbn: str, expected: bool):
    """
    Parametrized test demonstrating multiple test cases for ISBN validation.
    Shows how to test pure functions efficiently.
    """
    assert is_valid_isbn(isbn) == expected

@pytest.mark.parametrize("title,expected", [
    ("Valid Title", True),
    ("", False),
    (" ", False),
    ("A" * 200, True),
    ("A" * 201, False),
])
def test_title_validation(title: str, expected: bool):
    """Parametrized test for title validation."""
    assert is_valid_title(title) == expected

@pytest.mark.parametrize("days,expected_fee", [
    (0, 0.00),
    (1, 0.50),
    (10, 5.00),
    (100, 20.00),  # Should cap at MAX_FEE
])
def test_late_fee_calculation(days: int, expected_fee: float):
    """Parametrized test for late fee calculation."""
    assert calculate_late_fee(days) == expected_fee 