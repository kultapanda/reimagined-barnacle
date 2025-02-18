# Clean Code and Best Practices in Python

## Code Organization

### Package Structure
```
my_project/
├── src/
│   └── mypackage/
│       ├── __init__.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── models.py
│       │   └── services.py
│       ├── utils/
│       │   ├── __init__.py
│       │   └── helpers.py
│       └── api/
│           ├── __init__.py
│           └── routes.py
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   └── test_services.py
├── docs/
│   └── api.md
├── pyproject.toml
└── README.md
```

### Module Design
```python
"""
Module docstring explaining purpose and usage.

Example:
    >>> from mypackage.core import UserService
    >>> service = UserService()
    >>> service.create_user("alice@example.com")
"""

# Standard library imports
from datetime import datetime
from typing import Optional, List

# Third-party imports
import pandas as pd
from sqlalchemy import Column, String

# Local imports
from .models import User
from ..utils.validators import validate_email

# Constants
MAX_USERS = 1000
DEFAULT_TIMEOUT = 30

# Interface definitions
class UserRepository(Protocol):
    def save(self, user: User) -> None: ...
    def find_by_id(self, id: str) -> Optional[User]: ...

# Main implementation
class PostgresUserRepository:
    """Postgres implementation of UserRepository."""
    
    def __init__(self, connection_string: str):
        self._conn = connection_string
    
    def save(self, user: User) -> None:
        # Implementation
        pass

# Helper functions
def format_user_data(user: User) -> dict:
    """Format user data for API response."""
    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at.isoformat()
    }

# Main execution
if __name__ == "__main__":
    repo = PostgresUserRepository("postgresql://...")
```

### Dependency Management
```python
# pyproject.toml
[tool.poetry]
name = "mypackage"
version = "0.1.0"
description = "A clean Python package example"

[tool.poetry.dependencies]
python = "^3.9"
pandas = "^1.4.0"
sqlalchemy = "^1.4.0"

[tool.poetry.dev-dependencies]
pytest = "^7.0.0"
black = "^22.0.0"
mypy = "^0.950"

# requirements.txt (alternative)
pandas>=1.4.0,<2.0.0
sqlalchemy>=1.4.0,<2.0.0
```

## SOLID Principles in Python

### Single Responsibility
```python
# ❌ BAD: Class does too much
class User:
    def __init__(self, name: str):
        self.name = name
    
    def save(self) -> None:
        # Database logic here
        pass
    
    def send_email(self) -> None:
        # Email logic here
        pass

# ✅ GOOD: Separated responsibilities
class User:
    def __init__(self, name: str):
        self.name = name

class UserRepository:
    def save(self, user: User) -> None:
        # Database logic here
        pass

class EmailService:
    def send_email(self, user: User) -> None:
        # Email logic here
        pass
```

### Open/Closed
```python
# ❌ BAD: Need to modify class for new shapes
class AreaCalculator:
    def calculate_area(self, shape: str, params: dict) -> float:
        if shape == "rectangle":
            return params["width"] * params["height"]
        elif shape == "circle":
            return 3.14 * params["radius"] ** 2
        # Need to add more elif statements for new shapes

# ✅ GOOD: Open for extension, closed for modification
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def area(self) -> float:
        return self.width * self.height

class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius
    
    def area(self) -> float:
        return 3.14 * self.radius ** 2
```

### Liskov Substitution
```python
# ❌ BAD: Violates LSP
class Bird:
    def fly(self) -> None:
        pass

class Penguin(Bird):
    def fly(self) -> None:
        raise NotImplementedError("Penguins can't fly!")

# ✅ GOOD: Proper abstraction
class Bird(ABC):
    @abstractmethod
    def move(self) -> None:
        pass

class FlyingBird(Bird):
    def move(self) -> None:
        self.fly()
    
    def fly(self) -> None:
        pass

class SwimmingBird(Bird):
    def move(self) -> None:
        self.swim()
    
    def swim(self) -> None:
        pass
```

### Interface Segregation
```python
# ❌ BAD: Fat interface
class Worker(Protocol):
    def work(self) -> None: ...
    def eat(self) -> None: ...
    def sleep(self) -> None: ...

# ✅ GOOD: Segregated interfaces
class Workable(Protocol):
    def work(self) -> None: ...

class Eatable(Protocol):
    def eat(self) -> None: ...

class Sleepable(Protocol):
    def sleep(self) -> None: ...

class Human(Workable, Eatable, Sleepable):
    def work(self) -> None:
        pass
    
    def eat(self) -> None:
        pass
    
    def sleep(self) -> None:
        pass
```

### Dependency Inversion
```python
# ❌ BAD: High-level module depends on low-level module
class EmailSender:
    def send(self, message: str) -> None:
        # SMTP implementation
        pass

class NotificationService:
    def __init__(self):
        self.email_sender = EmailSender()
    
    def notify(self, message: str) -> None:
        self.email_sender.send(message)

# ✅ GOOD: Depends on abstraction
class MessageSender(Protocol):
    def send(self, message: str) -> None: ...

class EmailSender(MessageSender):
    def send(self, message: str) -> None:
        # SMTP implementation
        pass

class NotificationService:
    def __init__(self, sender: MessageSender):
        self.sender = sender
    
    def notify(self, message: str) -> None:
        self.sender.send(message)
```

## Code Quality

### Type Hints and Static Typing
```python
from typing import Optional, List, Dict, TypeVar, Generic

T = TypeVar('T')

class Repository(Generic[T]):
    def __init__(self) -> None:
        self.items: Dict[str, T] = {}
    
    def get(self, id: str) -> Optional[T]:
        return self.items.get(id)
    
    def save(self, id: str, item: T) -> None:
        self.items[id] = item
    
    def find_all(self) -> List[T]:
        return list(self.items.values())

# Usage with type checking
class User:
    def __init__(self, name: str) -> None:
        self.name = name

user_repo: Repository[User] = Repository()
user_repo.save("1", User("Alice"))
user: Optional[User] = user_repo.get("1")
```

### Documentation Standards
```python
class PaymentProcessor:
    """
    Handles payment processing and validation.
    
    This class provides methods for processing payments through
    various payment providers and ensures proper validation
    of payment data.
    
    Attributes:
        provider: The payment provider instance
        max_amount: Maximum allowed payment amount
    """
    
    def process_payment(
        self, 
        amount: float, 
        currency: str = "USD"
    ) -> bool:
        """
        Process a payment with the given amount and currency.
        
        Args:
            amount: The payment amount
            currency: The payment currency (default: "USD")
        
        Returns:
            bool: True if payment was successful, False otherwise
        
        Raises:
            ValueError: If amount is negative or exceeds max_amount
            PaymentError: If payment processing fails
        
        Example:
            >>> processor = PaymentProcessor()
            >>> processor.process_payment(100.00, "USD")
            True
        """
        if amount < 0:
            raise ValueError("Amount must be positive")
        # Implementation
        return True
```

### Linting and Formatting
```python
# pyproject.toml
[tool.black]
line-length = 88
target-version = ['py39']
include = '\.pyi?$'

[tool.isort]
profile = "black"
multi_line_output = 3

[tool.flake8]
max-line-length = 88
extend-ignore = "E203"

[tool.mypy]
python_version = "3.9"
strict = true
warn_return_any = true
warn_unused_configs = true

# Pre-commit configuration
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
  
  - repo: https://github.com/pycqa/isort
    rev: 5.10.1
    hooks:
      - id: isort
  
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.950
    hooks:
      - id: mypy
```

### Code Reviews
```python
# Example pull request template
"""
## Description
Brief description of changes

## Type of change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Type hints added
- [ ] Linting passes
- [ ] Pre-commit hooks pass

## Testing
Steps to test the changes:
1. Step 1
2. Step 2
3. Step 3

## Screenshots
If applicable, add screenshots
"""

# Code review comments examples
# ❌ BAD: Vague comment
# "This could be better"

# ✅ GOOD: Specific, actionable feedback
# "Consider using a dataclass here to reduce boilerplate and 
# make the data structure more explicit. Example:
# @dataclass
# class User:
#     name: str
#     email: str
# "
```

## Best Practices Summary

1. **Code Organization**
   - Follow consistent project structure
   - Keep modules focused and cohesive
   - Use proper dependency management

2. **SOLID Principles**
   - Single Responsibility: One reason to change
   - Open/Closed: Open for extension, closed for modification
   - Liskov Substitution: Subtypes must be substitutable
   - Interface Segregation: Small, focused interfaces
   - Dependency Inversion: Depend on abstractions

3. **Code Quality**
   - Use type hints consistently
   - Write clear documentation
   - Apply automatic formatting
   - Conduct thorough code reviews

## Exercises

1. **Code Organization**
```python
# Refactor this flat structure into proper modules
# TODO: Organize the following code into appropriate modules
```

2. **SOLID Principles**
```python
# Apply SOLID principles to this code
# TODO: Refactor following the SOLID principles
```

3. **Code Quality**
```python
# Add type hints and documentation
# TODO: Add proper typing and docstrings
``` 