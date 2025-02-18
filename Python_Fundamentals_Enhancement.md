# Python Fundamentals Enhancement

## Functions vs Classes: Making the Right Choice

### Functional Programming Concepts
- **Pure Functions**
  - Deterministic output based on input
  - No side effects
  - Examples:
    ```python
    # Pure function
    def add_numbers(a: int, b: int) -> int:
        return a + b

    # Impure function (has side effects)
    total = 0
    def add_to_total(n: int) -> int:
        global total
        total += n
        return total
    ```

- **First-Class Functions**
  - Functions as arguments
  - Functions as return values
  - Function composition
    ```python
    from typing import Callable

    def compose(f: Callable, g: Callable) -> Callable:
        return lambda x: f(g(x))

    def double(x: int) -> int:
        return x * 2

    def increment(x: int) -> int:
        return x + 1

    double_then_increment = compose(increment, double)
    ```

### When to Use Functions
1. **Data Transformation**
   - Processing streams of data
   - Map/filter/reduce operations
   ```python
   numbers = [1, 2, 3, 4, 5]
   doubled = map(lambda x: x * 2, numbers)
   evens = filter(lambda x: x % 2 == 0, numbers)
   ```

2. **Utility Operations**
   - Stateless operations
   - Helper functions
   ```python
   def validate_email(email: str) -> bool:
       import re
       pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
       return bool(re.match(pattern, email))
   ```

3. **Event Handlers**
   - Callback functions
   - Signal handlers
   ```python
   def on_button_click(event):
       print(f"Button clicked at position {event.position}")
   ```

### When to Choose Classes

1. **State Management**
   ```python
   class ShoppingCart:
       def __init__(self):
           self.items = []
           self.total = 0.0

       def add_item(self, item: dict) -> None:
           self.items.append(item)
           self.total += item['price']
   ```

2. **Encapsulation**
   ```python
   class DatabaseConnection:
       def __init__(self, connection_string: str):
           self._conn = None
           self._connection_string = connection_string

       def connect(self) -> None:
           # Implementation details hidden
           pass

       def execute_query(self, query: str) -> list:
           # Manages connection lifecycle internally
           pass
   ```

3. **Identity and Lifecycle Management**
   ```python
   class User:
       def __init__(self, user_id: str):
           self.user_id = user_id
           self.session = None

       def login(self) -> None:
           self.session = self._create_session()

       def logout(self) -> None:
           self.session.close()
           self.session = None
   ```

## Scoping and Namespaces

### LEGB Rule
1. **Local Scope**
   ```python
   def outer_function():
       x = "local"  # Local to outer_function
       def inner_function():
           y = "local"  # Local to inner_function
   ```

2. **Enclosing Scope**
   ```python
   def outer_function():
       x = "enclosing"
       def inner_function():
           print(x)  # Accesses enclosing scope
       return inner_function
   ```

3. **Global Scope**
   ```python
   global_var = "global"

   def some_function():
       global global_var
       global_var = "modified"  # Modifies global variable
   ```

4. **Built-in Scope**
   - Python's built-in functions and types
   - Always available without imports

### Module Organization

1. **Package Structure**
   ```
   my_package/
   ├── __init__.py
   ├── core.py
   ├── utils/
   │   ├── __init__.py
   │   ├── helpers.py
   │   └── validators.py
   └── tests/
       ├── __init__.py
       └── test_core.py
   ```

2. **Module Level Organization**
   ```python
   """Module docstring explaining purpose."""
   
   # Standard library imports
   import os
   import sys
   
   # Third-party imports
   import pandas as pd
   
   # Local imports
   from .utils import helpers
   
   # Constants
   MAX_RETRIES = 3
   
   # Classes
   class MyClass:
       pass
   
   # Functions
   def my_function():
       pass
   
   # Main execution
   if __name__ == "__main__":
       my_function()
   ```

### Import Best Practices

1. **Import Organization**
   ```python
   # Absolute imports (preferred)
   from my_package.utils import helpers
   
   # Relative imports (when necessary)
   from .utils import helpers
   ```

2. **Import Anti-patterns to Avoid**
   ```python
   # Bad: Star imports
   from module import *
   
   # Bad: Circular imports
   # file1.py
   from file2 import function2
   # file2.py
   from file1 import function1
   ```

3. **Lazy Imports**
   ```python
   def function_needing_heavy_module():
       # Import only when needed
       import heavy_module
       return heavy_module.process()
   ```

## Best Practices and Common Pitfalls

### Function Design
- Keep functions focused (Single Responsibility)
- Use type hints for clarity
- Document with docstrings
- Use default arguments carefully
  ```python
  # Bad
  def process_list(items=[]):  # Mutable default
      items.append(1)
  
  # Good
  def process_list(items=None):
      items = items or []
      items.append(1)
  ```

### Class Design
- Use dataclasses for data containers
  ```python
  from dataclasses import dataclass
  
  @dataclass
  class Point:
      x: float
      y: float
  ```
- Prefer composition over inheritance
- Implement special methods appropriately
- Use properties for computed attributes

Here's a clear comparison between methods and properties:
```python
class Rectangle:
    def __init__(self, width: float, height: float):
        self._width = width
        self._height = height
    
    # Method: Use when...
    def calculate_area(self) -> float:
        """
        - Complex calculations
        - Takes parameters
        - Changes state
        - Represents actions/behaviors
        """
        return self._width * self._height
    
    # Property: Use when...
    @property
    def area(self) -> float:
        """
        - Feels like data access
        - No parameters needed
        - Doesn't change state
        - Represents attributes/state
        """
        return self._width * self._height

# Method usage
rect = Rectangle(10, 20)
area1 = rect.calculate_area()  # Explicit call with ()
print(f"Method call syntax: {area1}")

# Property usage
area2 = rect.area  # Looks like attribute access
print(f"Property access syntax: {area2}")
```


Quick Decision Guide:
```python
# Use METHOD when:
def do_something(self, arg1, arg2):  # Takes arguments
    self.state_changes()              # Changes object state
    expensive_calculation()           # Heavy computation
    return complex_result            

# Use PROPERTY when:
@property
def something(self):                 # No arguments
    return self._x + self._y         # Simple computation
    # or return self._cached_value   # Cached value
```

Properties are essentially methods that pretend to be attributes. Use them when you want the syntax of attribute access but need the control of a method.

### Namespace Management
- Avoid polluting the global namespace

```python
# ❌ BAD: Global namespace pollution
from datetime import *
from pandas import *
from numpy import *

# Now we have conflicts and unclear origins
array([1, 2, 3])  # numpy or pandas?
now()  # which datetime function?

MAGIC_NUMBER = 42  # floating in global scope
def helper_function():  # utility floating in global scope
    pass


# ✅ GOOD: Controlled imports and scope
import datetime as dt
import numpy as np
from pandas import DataFrame, Series

# Clear origin of functions/classes
np.array([1, 2, 3])
dt.datetime.now()

class Config:
    """Constants contained in a class"""
    MAGIC_NUMBER = 42

def main():
    """Utilities scoped in functions or classes"""
    def helper_function():
        pass
    
    # Use helper within its scope
    helper_function()

if __name__ == "__main__":
    main()

# ❌ BAD: Star imports in __init__.py
# mypackage/__init__.py
from .module1 import *
from .module2 import *

# ✅ GOOD: Explicit imports in __init__.py
# mypackage/__init__.py
from .module1 import specific_function
from .module2 import SpecificClass

# ❌ BAD: Module-level side effects
# config.py
print("Loading config...")  # Side effect on import
DATABASE_URL = get_from_env()  # Side effect on import

# ✅ GOOD: Lazy loading and initialization
# config.py
class Config:
    @classmethod
    def init(cls):
        cls.DATABASE_URL = get_from_env()

# Use when needed
Config.init()
```
1. Key Principles:
1. Use explicit imports
1. Scope constants in classes
1. Keep utilities in appropriate classes/functions
1. Avoid module-level side effects
1. Use if __name__ == "__main__": for script entry points


- Use `__all__` to control exports

Here's a detailed explanation of `__all__` with examples:
```python
# mymodule.py
"""
✅ GOOD: Explicitly define public API
"""
__all__ = [
    'PublicClass',
    'public_function',
    'CONSTANT',
]

# Public items (included in __all__)
CONSTANT = 42

def public_function():
    return "I'm public!"

class PublicClass:
    pass

# Private items (not in __all__)
_INTERNAL_CONSTANT = 100

def _helper_function():
    pass

class _InternalClass:
    pass


# usage.py
# ✅ GOOD: Only imports what's in __all__
from mymodule import *
# Now you only have access to: PublicClass, public_function, CONSTANT

# ❌ BAD: No __all__ defined
from another_module import *  # Imports everything not starting with _


```


Real-world Example:
```python
# api.py
"""
Common pattern in libraries/frameworks
"""
__all__ = [
    # Core functionality
    'Client',
    'connect',
    
    # Exceptions
    'APIError',
    'ConnectionError',
    
    # Constants
    'DEFAULT_TIMEOUT',
    'API_VERSION',
]

class Client:
    pass

def connect():
    pass

class APIError(Exception):
    pass

class ConnectionError(Exception):
    pass

DEFAULT_TIMEOUT = 30
API_VERSION = '1.0'

# Internal stuff - not exported
_connection_pool = {}
def _validate_credentials():
    pass
```

Key Points:
1. `__all__` controls what's imported with `from module import *`
1. Makes the public API explicit
1. Best practice for library authors
1. Doesn't affect explicit imports (from module import specific_thing)
1. Helps with documentation generation


- Maintain clear module boundaries

Here's a guide to maintain clear module boundaries:
```python
# ❌ BAD: Mixed responsibilities
# utils.py
def parse_json(data): pass
def send_email(to, subject): pass
def calculate_tax(amount): pass
def resize_image(img): pass
def validate_user(user): pass

# ✅ GOOD: Clear module boundaries
# parsers.py
class JSONParser:
    def parse(self, data): pass

# notifications.py
class EmailService:
    def send(self, to, subject): pass

# finance/tax_calculator.py
class TaxCalculator:
    def calculate(self, amount): pass

# image/processor.py
class ImageProcessor:
    def resize(self, img): pass

# auth/validator.py
class UserValidator:
    def validate(self, user): pass
```

Example Project Structure:
```
myproject/
├── core/
│   ├── __init__.py
│   ├── models.py      # Core data models
│   └── exceptions.py  # Custom exceptions
├── services/
│   ├── __init__.py
│   ├── auth.py       # Authentication logic
│   └── payment.py    # Payment processing
├── utils/
│   ├── __init__.py
│   ├── formatters.py # Data formatting
│   └── validators.py # Input validation
└── api/
    ├── __init__.py
    ├── routes.py     # API endpoints
    └── schemas.py    # API data schemas
```

Key Principles:
1. Single Responsibility: Each module has one clear purpose
1. Encapsulation: Modules hide internal details
1. Dependencies: Clear, one-way dependency flow
1. Interface: Well-defined public APIs
1. Cohesion: Related functionality stays together


Example Usage:
```python
# ✅ GOOD: Clear dependencies
from core.models import User
from services.auth import AuthService
from services.payment import PaymentProcessor

class OrderManager:
    def __init__(self):
        self.auth = AuthService()
        self.payment = PaymentProcessor()

    def process_order(self, user: User, amount: float):
        if self.auth.verify(user):
            return self.payment.charge(amount)
```

- Use meaningful and consistent naming



Here's a comprehensive guide to Python naming conventions and best practices:
```python
# ❌ BAD: Unclear or inconsistent naming
def calc(x, y):
    return x + y

class data:
    def get_the_thing(self): pass
    def process(self): pass
    def handle_stuff_with_other_things(self): pass

my_l = [1, 2, 3]
tmp = 42
flag = True


# ✅ GOOD: Clear, consistent, meaningful names
def calculate_total(price: float, tax_rate: float) -> float:
    return price * (1 + tax_rate)

class OrderProcessor:
    def get_order_status(self) -> str: pass
    def process_payment(self) -> bool: pass
    def handle_shipping_notification(self) -> None: pass

prices = [1, 2, 3]
max_retries = 42
is_active = True
```

Naming Conventions:
```python
# Variables and Functions: lowercase_with_underscores
user_id = 42
def validate_email(email: str) -> bool: pass

# Classes: PascalCase
class UserAccount: pass
class PaymentProcessor: pass

# Constants: UPPERCASE_WITH_UNDERSCORES
MAX_CONNECTIONS = 100
DEFAULT_TIMEOUT = 30

# Protected/Private: _single_leading_underscore
class User:
    def __init__(self):
        self._password = None  # Protected
        self.__secret = None   # Private (name mangling)

# Special Methods: __double_underscores__
def __init__(self): pass
def __str__(self): pass

# Type Variables: CapitalizedSingle
from typing import TypeVar
T = TypeVar('T')
```



Common Patterns:
```python
# Boolean variables/functions: is_, has_, can_, should_
is_valid = True
has_permission = False
def is_authenticated(user): pass

# Collections: plural nouns
users = ['alice', 'bob']
error_codes = {404, 500}
price_mapping = {'basic': 10, 'premium': 20}

# Callbacks/Handlers: _handler, _callback
def on_click_handler(event): pass
def data_received_callback(data): pass

# Factory functions: create_, make_, build_
def create_user(name): pass
def make_request(url): pass

# Context managers: with_ prefix
@contextmanager
def with_transaction(): pass
```

Best Practices:
1. Be descriptive but concise
1. Use technical terms correctly
1. Be consistent across the codebase
1. Avoid abbreviations unless very common
1. Make names searchable
1. Use opposites consistently (start/stop, open/close)



## Exercises and Examples

1. **Function vs Class Decision Exercise**
   ```python
   # Convert this function-based code to OOP if appropriate
   
   def process_order(order_items, customer_info):
       total = sum(item['price'] for item in order_items)
       # More processing...
   
   # Potential OOP solution
   class Order:
       def __init__(self, items, customer):
           self.items = items
           self.customer = customer
           self._total = None
   
       @property
       def total(self):
           if self._total is None:
               self._total = sum(item['price'] for item in self.items)
           return self._total
   ```

2. **Scope Understanding Exercise**
   ```python
   # Predict the output
   x = 1
   def outer():
       x = 2
       def inner():
           x = 3
           print(f"Inner x: {x}")
       inner()
       print(f"Outer x: {x}")
   outer()
   print(f"Global x: {x}")
   ```

3. **Module Organization Exercise**
   - Organize a given set of functions and classes into appropriate modules
   - Design proper import hierarchy
   - Implement circular dependency solutions 