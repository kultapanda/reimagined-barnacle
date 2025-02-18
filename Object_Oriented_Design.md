# Object-Oriented Design in Python

## OOP Fundamentals in Python

### Inheritance vs Composition
```python
# ❌ Inheritance when composition would be better
class FileSystem:
    def read(self): pass
    def write(self): pass

class Database(FileSystem):  # Inheritance
    def query(self): pass
    # Now Database has read/write methods it shouldn't expose

# ✅ Composition instead
class Database:
    def __init__(self):
        self._storage = FileSystem()  # Composition
    
    def query(self):
        data = self._storage.read()
        # Process data
        return result
```

### Abstract Classes and Interfaces
```python
from abc import ABC, abstractmethod
from typing import Protocol

# Method 1: Abstract Base Class
class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        """Process a payment."""
        pass
    
    @abstractmethod
    def refund(self, amount: float) -> bool:
        """Process a refund."""
        pass

# Method 2: Protocol (Structural Subtyping)
class DataStore(Protocol):
    def save(self, data: dict) -> None: ...
    def load(self, id: str) -> dict: ...

# Implementation
class SQLiteStore:
    def save(self, data: dict) -> None:
        # Implementation
        pass
    
    def load(self, id: str) -> dict:
        # Implementation
        pass

# Type checking will pass
def save_user(store: DataStore, user_data: dict) -> None:
    store.save(user_data)
```

### Multiple Inheritance and MRO
```python
class Loggable:
    def log(self, message):
        print(f"Log: {message}")

class Serializable:
    def serialize(self):
        return str(self.__dict__)

class User(Loggable, Serializable):
    def __init__(self, name):
        self.name = name
    
    def save(self):
        self.log(f"Saving user {self.name}")
        data = self.serialize()
        # Save data

# Diamond Problem Example
class A:
    def method(self): print("A")

class B(A):
    def method(self): print("B")

class C(A):
    def method(self): print("C")

class D(B, C):
    pass  # Python's MRO determines method resolution
```

### Properties and Descriptors
```python
class Temperature:
    def __init__(self):
        self._celsius = 0
    
    @property
    def celsius(self):
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Temperature below absolute zero!")
        self._celsius = value
    
    @property
    def fahrenheit(self):
        return (self.celsius * 9/5) + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = (value - 32) * 5/9

# Custom Descriptor
class ValidString:
    def __init__(self, minlen=0):
        self.minlen = minlen
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get('_name', '')
    
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError('Value must be string')
        if len(value) < self.minlen:
            raise ValueError(f'String must be at least {self.minlen} chars')
        instance.__dict__['_name'] = value

class User:
    name = ValidString(minlen=3)  # Using descriptor
```

## Design Patterns

### Creational Patterns
```python
# Singleton
class Configuration:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# Factory Method
class DocumentFactory:
    @staticmethod
    def create_document(type_: str):
        if type_ == "pdf":
            return PDFDocument()
        elif type_ == "word":
            return WordDocument()
        raise ValueError(f"Unknown document type: {type_}")

# Builder
class ComputerBuilder:
    def __init__(self):
        self.computer = Computer()
    
    def add_cpu(self, cpu):
        self.computer.cpu = cpu
        return self
    
    def add_memory(self, memory):
        self.computer.memory = memory
        return self
    
    def build(self):
        return self.computer
```

### Structural Patterns
```python
# Adapter
class LegacyPrinter:
    def print_old(self, text): pass

class PrinterAdapter:
    def __init__(self, legacy_printer):
        self.printer = legacy_printer
    
    def print(self, text):  # New interface
        self.printer.print_old(text)  # Old interface

# Decorator
from functools import wraps

def log_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Finished {func.__name__}")
        return result
    return wrapper

# Composite
class Component:
    @abstractmethod
    def operation(self): pass

class Leaf(Component):
    def operation(self):
        return "Leaf"

class Composite(Component):
    def __init__(self):
        self._children = []
    
    def add(self, component):
        self._children.append(component)
    
    def operation(self):
        results = []
        for child in self._children:
            results.append(child.operation())
        return f"Branch({', '.join(results)})"
```

### Behavioral Patterns
```python
# Observer
class Subject:
    def __init__(self):
        self._observers = []
        self._state = None
    
    def attach(self, observer):
        self._observers.append(observer)
    
    def notify(self):
        for observer in self._observers:
            observer.update(self._state)

# Strategy
from typing import Callable

class SortStrategy:
    def __init__(self, strategy: Callable):
        self.strategy = strategy
    
    def sort(self, data):
        return self.strategy(data)

# Quick sort strategy
def quick_sort(data):
    # Implementation
    pass

# Merge sort strategy
def merge_sort(data):
    # Implementation
    pass

# Usage
sorter = SortStrategy(quick_sort)
sorted_data = sorter.sort(data)
```

## Python-Specific OOP

### Dunder Methods
```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)
    
    def __str__(self):
        return f"Vector({self.x}, {self.y})"
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __len__(self):
        return int((self.x ** 2 + self.y ** 2) ** 0.5)
```

### Metaclasses
```python
class ValidationMeta(type):
    def __new__(cls, name, bases, attrs):
        # Add validation to all methods
        for key, value in attrs.items():
            if callable(value) and not key.startswith('__'):
                attrs[key] = cls.validate_types(value)
        return super().__new__(cls, name, bases, attrs)
    
    @staticmethod
    def validate_types(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Perform validation
            return func(*args, **kwargs)
        return wrapper

class ValidatedClass(metaclass=ValidationMeta):
    def process_data(self, data: dict) -> list:
        return list(data.values())
```

### Protocols and ABCs
```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> None: ...

class Circle:
    def draw(self) -> None:
        print("Drawing circle")

class Square:
    def draw(self) -> None:
        print("Drawing square")

def draw_shapes(shapes: list[Drawable]) -> None:
    for shape in shapes:
        shape.draw()

# This works because Circle and Square implement draw()
shapes = [Circle(), Square()]
draw_shapes(shapes)
```

## Comparison with Java/C# OOP Models
```python
# Python's approach to interfaces
from typing import Protocol

class Comparable(Protocol):
    def __lt__(self, other) -> bool: ...

# vs Java's explicit interface
"""
public interface Comparable<T> {
    public int compareTo(T other);
}
"""

# Python's multiple inheritance
class A: pass
class B: pass
class C(A, B): pass  # Multiple inheritance

# vs Java's single inheritance with interfaces
"""
public class C extends A implements B {
    // Implementation
}
"""

# Python's properties
class Person:
    @property
    def name(self): return self._name

# vs C# properties
"""
public class Person {
    public string Name { get; set; }
}
"""
```

## Best Practices

### SOLID Principles in Python
```python
# Single Responsibility
class UserAuth:
    def authenticate(self, credentials): pass

class UserProfile:
    def update_profile(self, data): pass

# Open/Closed
class DiscountCalculator:
    def calculate(self, order: Order) -> float:
        return order.calculate_discount()  # Polymorphic behavior

# Liskov Substitution
class Bird:
    def fly(self): pass

class Penguin(Bird):  # ❌ Violates LSP
    def fly(self):
        raise NotImplementedError("Penguins can't fly")

# Interface Segregation
class Worker(Protocol):
    def work(self): ...

class Eater(Protocol):
    def eat(self): ...

# Dependency Inversion
class ReportGenerator:
    def __init__(self, storage: DataStore):  # Depends on abstraction
        self.storage = storage
```

### Error Handling
```python
class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

def process_user_input(data: dict) -> None:
    try:
        validate_input(data)
        process_data(data)
    except ValidationError as e:
        logger.error(f"Validation failed: {e}")
        raise
    except Exception as e:
        logger.critical(f"Unexpected error: {e}")
        raise ProcessingError("Failed to process input") from e
```

## Exercises

1. **Design Pattern Implementation**
```python
# Implement a logging system using the Observer pattern
# TODO: Create Subject and Observer classes
```

2. **SOLID Principles Practice**
```python
# Refactor this code to follow SOLID principles
# TODO: Split UserManager into smaller, focused classes
```

3. **Custom Collection**
```python
# Implement a custom collection with proper dunder methods
# TODO: Create a Stack class with __len__, __iter__, etc.
``` 