# Testing Fundamentals in Python

## Unit Testing Philosophy

### Test-Driven Development (TDD)
- **Red-Green-Refactor Cycle**
  ```python
  # 1. Red: Write a failing test
  def test_user_creation():
      user = User("alice@email.com")
      assert user.email == "alice@email.com"
      assert user.is_active == False  # Fails - User class doesn't exist yet

  # 2. Green: Write minimal code to pass
  class User:
      def __init__(self, email):
          self.email = email
          self.is_active = False

  # 3. Refactor: Improve implementation
  class User:
      def __init__(self, email):
          self._validate_email(email)
          self.email = email
          self.is_active = False
      
      def _validate_email(self, email):
          if '@' not in email:
              raise ValueError("Invalid email format")
  ```

### Behavior-Driven Development (BDD)
```python
from pytest_bdd import scenario, given, when, then

@scenario('features/checkout.feature', 'Add item to cart')
def test_add_to_cart():
    pass

@given("a user with an empty shopping cart")
def empty_cart():
    return ShoppingCart()

@when("they add a product costing $10")
def add_product(empty_cart):
    empty_cart.add_item({"name": "Test Product", "price": 10})

@then("the cart total should be $10")
def check_total(empty_cart):
    assert empty_cart.total == 10
```

## PyTest Deep Dive

### Fixtures and Their Proper Use
```python
import pytest
from datetime import datetime

@pytest.fixture
def active_user():
    """Provides a pre-configured user for testing."""
    return User(
        email="test@example.com",
        is_active=True,
        created_at=datetime.now()
    )

@pytest.fixture
def db_session():
    """Provides a database session with automatic cleanup."""
    session = create_session()
    yield session
    session.close()  # Cleanup after test

def test_user_deactivation(active_user, db_session):
    active_user.deactivate()
    assert not active_user.is_active
    db_session.commit()
```

### Parametrization
```python
@pytest.mark.parametrize("email,is_valid", [
    ("user@example.com", True),
    ("invalid-email", False),
    ("user@.com", False),
    ("user@domain.com", True),
])
def test_email_validation(email, is_valid):
    if is_valid:
        User(email=email)  # Should not raise
    else:
        with pytest.raises(ValueError):
            User(email=email)

@pytest.mark.parametrize("items,expected_total", [
    ([], 0),
    ([{"price": 10}], 10),
    ([{"price": 10}, {"price": 20}], 30),
])
def test_cart_total(items, expected_total):
    cart = ShoppingCart()
    for item in items:
        cart.add_item(item)
    assert cart.total == expected_total
```

### Mocking and Patching
```python
from unittest.mock import Mock, patch

def test_payment_processing():
    # Method 1: Mock object
    mock_gateway = Mock()
    mock_gateway.process_payment.return_value = True
    
    payment = Payment(gateway=mock_gateway)
    assert payment.process(100)

    mock_gateway.process_payment.assert_called_once_with(100)

    # Method 2: Patch decorator
    @patch('myapp.services.PaymentGateway')
    def test_payment_integration(mock_gateway):
        mock_gateway.return_value.process_payment.return_value = True
        payment = Payment()
        assert payment.process(100)

    # Method 3: Context manager
    def test_external_api():
        with patch('requests.post') as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {"status": "success"}
            
            service = ExternalService()
            result = service.send_data({"key": "value"})
            assert result["status"] == "success"
```

### Test Organization Patterns
```python
# test_user.py
class TestUser:
    """Group related user tests"""
    
    def test_creation(self):
        user = User("test@example.com")
        assert user.email == "test@example.com"
    
    def test_validation(self):
        with pytest.raises(ValueError):
            User("invalid-email")
    
    class TestAuthentication:
        """Nested class for auth-specific tests"""
        
        def test_login(self, active_user):
            assert active_user.login("password")
        
        def test_logout(self, active_user):
            active_user.logout()
            assert not active_user.is_logged_in

# test_integration/test_payment.py
@pytest.mark.integration
class TestPaymentIntegration:
    """Integration tests marked separately"""
    
    def test_full_payment_flow(self, db_session):
        # Test entire payment process
        pass
```

### Coverage Analysis
```bash
# Command line usage
pytest --cov=myapp --cov-report=html tests/
```

```python
# .coveragerc
[run]
source = myapp
omit = 
    */migrations/*
    */tests/*
    */__init__.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
```

## Testing Patterns

### Arrange-Act-Assert
```python
def test_order_processing():
    # Arrange
    order = Order()
    product = Product("Test Product", 100)
    
    # Act
    order.add_product(product)
    order.process()
    
    # Assert
    assert order.is_processed
    assert order.total == 100
```

### Given-When-Then
```python
def test_refund_process():
    # Given
    order = create_processed_order()
    
    # When
    refund = order.refund()
    
    # Then
    assert refund.status == "completed"
    assert order.status == "refunded"
```

### Test Doubles
```python
# 1. Stub: Returns fixed values
class PaymentGatewayStub:
    def process_payment(self, amount):
        return True

# 2. Spy: Records calls
class PaymentGatewaySpy:
    def __init__(self):
        self.process_payment_calls = []
    
    def process_payment(self, amount):
        self.process_payment_calls.append(amount)
        return True

# 3. Mock: Verifies behavior
class PaymentGatewayMock:
    def __init__(self, expected_amount):
        self.expected_amount = expected_amount
        self.called = False
    
    def process_payment(self, amount):
        assert amount == self.expected_amount
        self.called = True
        return True
    
    def verify(self):
        assert self.called, "Expected process_payment to be called"

# 4. Fake: Working implementation
class InMemoryRepository:
    def __init__(self):
        self.items = {}
    
    def save(self, item):
        self.items[item.id] = item
    
    def get(self, id):
        return self.items.get(id)
```

## Best Practices

### Test Structure
```python
# ✅ GOOD: Clear test structure
def test_order_cancellation():
    # Setup
    order = create_test_order()
    
    # Exercise
    result = order.cancel()
    
    # Verify
    assert result.success
    assert order.status == "cancelled"
    assert len(order.cancellation_events) == 1

# ❌ BAD: Unclear test
def test_cancel():
    o = Order()
    o.cancel()
    assert o.s == "cancelled"
```

### Naming Conventions
```python
# ✅ GOOD: Descriptive test names
def test_order_total_includes_tax()
def test_inactive_user_cannot_login()
def test_email_validation_rejects_invalid_format()

# ❌ BAD: Vague test names
def test_total()
def test_login()
def test_validation()
```

### Test Independence
```python
# ✅ GOOD: Independent tests
class TestOrder:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.order = Order()
    
    def test_add_item(self):
        self.order.add_item(Item("test", 10))
        assert len(self.order.items) == 1
    
    def test_remove_item(self):
        item = Item("test", 10)
        self.order.add_item(item)
        self.order.remove_item(item)
        assert len(self.order.items) == 0

# ❌ BAD: Dependent tests
def test_order_flow():
    order = Order()
    order.add_item(Item("test", 10))  # Test 1
    assert len(order.items) == 1
    
    order.process()  # Test 2
    assert order.is_processed
    
    order.cancel()  # Test 3
    assert order.is_cancelled
```

## Exercises

1. **TDD Exercise: Shopping Cart**
```python
# Implement shopping cart with TDD
def test_empty_cart_total():
    cart = ShoppingCart()
    assert cart.total == 0

def test_add_item_updates_total():
    cart = ShoppingCart()
    cart.add_item({"price": 10})
    assert cart.total == 10
```

2. **Mocking Exercise: Payment Service**
```python
# Practice different mocking strategies
def test_payment_service():
    # TODO: Implement test using different mock types
    pass
```

3. **Integration Test Exercise: Order System**
```python
# Write integration tests for order processing
@pytest.mark.integration
def test_complete_order_flow():
    # TODO: Test order creation through completion
    pass
``` 