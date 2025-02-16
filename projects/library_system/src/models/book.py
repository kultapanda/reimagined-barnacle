from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Book:
    """
    Represents a book in the library system.
    Uses a class because books have state (availability, due date) that needs to be managed.
    """
    isbn: str
    title: str
    author: str
    is_available: bool = True
    due_date: Optional[datetime] = None

    def check_out(self, return_days: int = 14) -> datetime:
        """
        Changes book state to checked out and calculates due date.
        Uses a method because it modifies object state.
        """
        if not self.is_available:
            raise ValueError("Book is already checked out")
        
        from datetime import timedelta
        self.is_available = False
        self.due_date = datetime.now() + timedelta(days=return_days)
        return self.due_date

    def return_book(self) -> None:
        """
        Changes book state to available.
        Uses a method because it modifies object state.
        """
        self.is_available = True
        self.due_date = None 