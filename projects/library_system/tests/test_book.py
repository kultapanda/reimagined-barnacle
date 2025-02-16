import pytest
from datetime import datetime, timedelta
from src.models.book import Book

@pytest.fixture
def sample_book():
    """Fixture providing a test book instance."""
    return Book(
        isbn="1234567890",
        title="Test Book",
        author="Test Author"
    )

def test_book_initial_state(sample_book):
    """Test the initial state of a new book."""
    assert sample_book.is_available
    assert sample_book.due_date is None

def test_book_checkout(sample_book):
    """Test book checkout process."""
    # Arrange
    return_days = 14
    
    # Act
    due_date = sample_book.check_out(return_days)
    
    # Assert
    assert not sample_book.is_available
    assert isinstance(due_date, datetime)
    assert due_date.date() == (datetime.now() + timedelta(days=return_days)).date()

def test_book_return(sample_book):
    """Test book return process."""
    # Arrange
    sample_book.check_out()
    
    # Act
    sample_book.return_book()
    
    # Assert
    assert sample_book.is_available
    assert sample_book.due_date is None

def test_cannot_checkout_unavailable_book(sample_book):
    """Test that checking out an unavailable book raises an error."""
    # Arrange
    sample_book.check_out()
    
    # Act/Assert
    with pytest.raises(ValueError, match="Book is already checked out"):
        sample_book.check_out() 