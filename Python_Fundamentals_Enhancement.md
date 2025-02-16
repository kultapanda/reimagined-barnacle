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

### Namespace Management
- Avoid polluting the global namespace
- Use `__all__` to control exports
- Maintain clear module boundaries
- Use meaningful and consistent naming

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