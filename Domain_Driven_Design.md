# Domain-Driven Design in Python

## DDD Fundamentals

### Ubiquitous Language
```python
# ❌ BAD: Inconsistent terminology
class UserAccount:
    def modify_balance(self, amount): pass
    def update_customer_info(self): pass
    def change_status(self): pass

# ✅ GOOD: Consistent domain language
class BankAccount:
    def deposit(self, amount: Decimal) -> None: pass
    def withdraw(self, amount: Decimal) -> None: pass
    def freeze(self) -> None: pass
```

### Value Objects
```python
from dataclasses import dataclass
from typing import NewType

@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str
    
    def __add__(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)

# Using NewType for type safety
AccountId = NewType('AccountId', str)
CustomerId = NewType('CustomerId', str)

# Now these are different types:
account_id: AccountId = AccountId("A123")
customer_id: CustomerId = CustomerId("C123")
```

### Entities
```python
class Account:
    def __init__(self, account_id: AccountId, owner: CustomerId):
        self._id = account_id
        self._owner = owner
        self._balance = Money(Decimal("0"), "USD")
        self._transactions: List[Transaction] = []
    
    def deposit(self, amount: Money) -> None:
        if amount.currency != self._balance.currency:
            raise ValueError("Currency mismatch")
        
        transaction = Transaction.create_deposit(
            account_id=self._id,
            amount=amount
        )
        self._transactions.append(transaction)
        self._balance += amount
```

### Aggregates
```python
class Customer:
    def __init__(self, id: CustomerId):
        self._id = id
        self._accounts: Dict[AccountId, Account] = {}
    
    def open_account(self, account_type: AccountType) -> Account:
        """Opens a new account for the customer."""
        account = Account(
            account_id=AccountId(str(uuid4())),
            owner=self._id
        )
        self._accounts[account.id] = account
        return account
    
    def get_total_balance(self) -> Money:
        """Calculates total balance across all accounts."""
        return sum(
            (account.balance for account in self._accounts.values()),
            start=Money(Decimal("0"), "USD")
        )
```

## Strategic Design

### Bounded Contexts
```python
# Banking Context
class Account:
    def deposit(self, amount: Money) -> None: pass
    def withdraw(self, amount: Money) -> None: pass

# Risk Management Context
class AccountRiskProfile:
    def calculate_risk_score(self) -> int: pass
    def flag_suspicious_activity(self) -> None: pass

# Customer Service Context
class AccountEnquiry:
    def get_transaction_history(self) -> List[Transaction]: pass
    def get_statement(self, month: int, year: int) -> Statement: pass
```

### Context Mapping
```python
# Upstream Context (Core Banking)
class CoreBankingAccount:
    def __init__(self, account_id: AccountId):
        self._id = account_id
        self._balance = Money(Decimal("0"), "USD")
    
    def apply_transaction(self, transaction: Transaction) -> None:
        # Core banking logic
        pass

# Downstream Context (Customer Service) with Anti-Corruption Layer
class CustomerServiceAccount:
    def __init__(self, core_account: CoreBankingAccount):
        self._core_account = core_account
        self._acl = AccountAntiCorruptionLayer()
    
    def get_balance(self) -> dict:
        # Convert internal domain model to customer service format
        return self._acl.translate_balance(self._core_account._balance)

class AccountAntiCorruptionLayer:
    def translate_balance(self, balance: Money) -> dict:
        return {
            "amount": float(balance.amount),
            "currency": balance.currency,
            "formatted": f"{balance.currency} {balance.amount:,.2f}"
        }
```

### Subdomains
```python
# Core Subdomain (Essential Banking)
class CoreBanking:
    def process_transaction(self, transaction: Transaction) -> None:
        # Critical business logic
        pass

# Supporting Subdomain (Reporting)
class ReportingService:
    def generate_monthly_statement(self, account: Account) -> PDF:
        # Important but not core business logic
        pass

# Generic Subdomain (Email Notifications)
class NotificationService:
    def send_transaction_notification(self, transaction: Transaction) -> None:
        # Could be replaced with third-party service
        pass
```

## Tactical Design

### Domain Events
```python
@dataclass(frozen=True)
class DomainEvent:
    occurred_on: datetime

@dataclass(frozen=True)
class AccountOpened(DomainEvent):
    account_id: AccountId
    owner_id: CustomerId
    account_type: AccountType

@dataclass(frozen=True)
class FundsDeposited(DomainEvent):
    account_id: AccountId
    amount: Money
    balance_after: Money

class Account:
    def __init__(self, id: AccountId, owner: CustomerId):
        self._id = id
        self._owner = owner
        self._balance = Money(Decimal("0"), "USD")
        self._events: List[DomainEvent] = []
    
    def deposit(self, amount: Money) -> None:
        self._balance += amount
        self._events.append(FundsDeposited(
            occurred_on=datetime.now(),
            account_id=self._id,
            amount=amount,
            balance_after=self._balance
        ))
```

### Repositories
```python
class AccountRepository(Protocol):
    def save(self, account: Account) -> None: ...
    def find_by_id(self, id: AccountId) -> Optional[Account]: ...
    def find_by_owner(self, owner_id: CustomerId) -> List[Account]: ...

class PostgresAccountRepository:
    def __init__(self, session: Session):
        self._session = session
    
    def save(self, account: Account) -> None:
        # Convert domain model to database model
        db_account = AccountModel.from_domain(account)
        self._session.merge(db_account)
        self._session.commit()
    
    def find_by_id(self, id: AccountId) -> Optional[Account]:
        db_account = self._session.query(AccountModel).get(id)
        return db_account.to_domain() if db_account else None
```

### Domain Services
```python
class MoneyTransferService:
    def __init__(
        self,
        account_repository: AccountRepository,
        exchange_rate_service: ExchangeRateService
    ):
        self._accounts = account_repository
        self._exchange = exchange_rate_service
    
    def transfer(
        self,
        from_account_id: AccountId,
        to_account_id: AccountId,
        amount: Money
    ) -> None:
        """
        Handles money transfer between accounts, including currency conversion.
        """
        from_account = self._accounts.find_by_id(from_account_id)
        to_account = self._accounts.find_by_id(to_account_id)
        
        if not from_account or not to_account:
            raise AccountNotFoundError()
        
        if from_account.currency != amount.currency:
            raise InvalidCurrencyError()
        
        # Convert if currencies differ
        if from_account.currency != to_account.currency:
            converted_amount = self._exchange.convert(
                amount,
                to_account.currency
            )
        else:
            converted_amount = amount
        
        # Perform transfer
        from_account.withdraw(amount)
        to_account.deposit(converted_amount)
        
        # Save changes
        self._accounts.save(from_account)
        self._accounts.save(to_account)
```

## Best Practices

### Implementing DDD in Python
```python
# 1. Use type hints for better domain modeling
from typing import NewType, List, Optional
from dataclasses import dataclass
from datetime import datetime

# 2. Make invalid states unrepresentable
@dataclass(frozen=True)
class EmailAddress:
    value: str
    
    def __post_init__(self):
        if not self._is_valid_email(self.value):
            raise ValueError("Invalid email address")
    
    @staticmethod
    def _is_valid_email(email: str) -> bool:
        # Email validation logic
        pass

# 3. Use domain events for side effects
class Account:
    def withdraw(self, amount: Money) -> None:
        if amount > self._balance:
            raise InsufficientFundsError()
        
        self._balance -= amount
        self._events.append(
            FundsWithdrawn(
                account_id=self.id,
                amount=amount,
                balance_after=self._balance
            )
        )
```

### Testing DDD Code
```python
def test_money_transfer_service():
    # Arrange
    from_account = Account(AccountId("A1"), CustomerId("C1"))
    to_account = Account(AccountId("A2"), CustomerId("C2"))
    amount = Money(Decimal("100"), "USD")
    
    repository = InMemoryAccountRepository()
    repository.save(from_account)
    repository.save(to_account)
    
    exchange_service = MockExchangeRateService()
    transfer_service = MoneyTransferService(repository, exchange_service)
    
    # Act
    transfer_service.transfer(from_account.id, to_account.id, amount)
    
    # Assert
    assert from_account.balance == Money(Decimal("0"), "USD")
    assert to_account.balance == Money(Decimal("100"), "USD")
```

## Exercises

1. **Domain Modeling**
```python
# Model a simple e-commerce domain
# Include concepts like:
# - Order
# - Product
# - Customer
# - Shopping Cart
```

2. **Event Sourcing**
```python
# Implement event sourcing for the Account aggregate
# Track all state changes through events
```

3. **Bounded Context Integration**
```python
# Create an anti-corruption layer between
# Shipping and Inventory contexts
``` 