# Advanced Architecture in Python

## Application Architecture

### Layered Architecture
```python
# 1. Presentation Layer
class OrderController:
    def __init__(self, order_service: OrderService):
        self._service = order_service
    
    def create_order(self, request_data: dict) -> dict:
        """HTTP endpoint for order creation."""
        try:
            order = self._service.create_order(
                customer_id=request_data['customer_id'],
                items=request_data['items']
            )
            return {"order_id": str(order.id), "status": "created"}
        except ValidationError as e:
            return {"error": str(e)}, 400

# 2. Application Layer
class OrderService:
    def __init__(
        self,
        order_repository: OrderRepository,
        product_service: ProductService,
        payment_service: PaymentService
    ):
        self._orders = order_repository
        self._products = product_service
        self._payments = payment_service
    
    def create_order(self, customer_id: str, items: List[dict]) -> Order:
        """Coordinates the order creation process."""
        # Validate products
        product_ids = [item['product_id'] for item in items]
        if not self._products.are_available(product_ids):
            raise ValidationError("Some products are unavailable")
        
        # Create order
        order = Order.create(customer_id, items)
        self._orders.save(order)
        
        # Process payment
        self._payments.process(order)
        return order

# 3. Domain Layer
class Order:
    def __init__(self, id: OrderId, customer_id: CustomerId):
        self.id = id
        self.customer_id = customer_id
        self._items: List[OrderItem] = []
        self._status = OrderStatus.PENDING
    
    @classmethod
    def create(cls, customer_id: str, items: List[dict]) -> 'Order':
        order = cls(OrderId(uuid4()), CustomerId(customer_id))
        for item in items:
            order.add_item(item)
        return order

# 4. Infrastructure Layer
class PostgresOrderRepository:
    def __init__(self, session: Session):
        self._session = session
    
    def save(self, order: Order) -> None:
        db_order = OrderModel.from_domain(order)
        self._session.add(db_order)
        self._session.commit()
```

### Hexagonal Architecture (Ports & Adapters)
```python
# Core Domain (Application Core)
class OrderService:
    def __init__(self, order_repository: OrderRepository):
        self._repository = order_repository
    
    def place_order(self, order_data: OrderData) -> Order:
        order = Order.create(order_data)
        self._repository.save(order)
        return order

# Ports (Interfaces)
class OrderRepository(Protocol):
    def save(self, order: Order) -> None: ...
    def find_by_id(self, id: OrderId) -> Optional[Order]: ...

class PaymentGateway(Protocol):
    def process_payment(self, amount: Money) -> bool: ...

# Primary Adapters (Driving Adapters)
class OrderRestController:
    def __init__(self, order_service: OrderService):
        self._service = order_service
    
    def handle_post(self, request: HttpRequest) -> HttpResponse:
        order_data = OrderData.from_request(request)
        order = self._service.place_order(order_data)
        return JsonResponse({"order_id": str(order.id)})

class OrderGraphQLResolver:
    def __init__(self, order_service: OrderService):
        self._service = order_service
    
    def resolve_create_order(self, info, input_data):
        order_data = OrderData.from_graphql(input_data)
        order = self._service.place_order(order_data)
        return CreateOrderPayload(order=order)

# Secondary Adapters (Driven Adapters)
class SqlAlchemyOrderRepository:
    def __init__(self, session: Session):
        self._session = session
    
    def save(self, order: Order) -> None:
        db_order = OrderModel.from_domain(order)
        self._session.add(db_order)
        self._session.commit()

class StripePaymentGateway:
    def __init__(self, api_key: str):
        self._stripe = stripe.Client(api_key)
    
    def process_payment(self, amount: Money) -> bool:
        try:
            self._stripe.charges.create(
                amount=amount.value,
                currency=amount.currency.lower()
            )
            return True
        except stripe.error.StripeError:
            return False
```

### Event-Driven Architecture
```python
# Events
@dataclass(frozen=True)
class OrderPlaced:
    order_id: OrderId
    customer_id: CustomerId
    items: List[OrderItem]
    total: Money

@dataclass(frozen=True)
class PaymentProcessed:
    order_id: OrderId
    amount: Money
    transaction_id: str

# Event Bus
class EventBus:
    def __init__(self):
        self._handlers: Dict[Type[Event], List[Callable]] = defaultdict(list)
    
    def subscribe(self, event_type: Type[Event], handler: Callable) -> None:
        self._handlers[event_type].append(handler)
    
    def publish(self, event: Event) -> None:
        for handler in self._handlers[type(event)]:
            handler(event)

# Event Handlers
class OrderProcessor:
    def __init__(self, payment_service: PaymentService):
        self._payments = payment_service
    
    def handle_order_placed(self, event: OrderPlaced) -> None:
        payment_result = self._payments.process_payment(
            order_id=event.order_id,
            amount=event.total
        )
        if payment_result.success:
            event_bus.publish(PaymentProcessed(
                order_id=event.order_id,
                amount=event.total,
                transaction_id=payment_result.transaction_id
            ))

# Event Sourcing
class OrderAggregate:
    def __init__(self, id: OrderId):
        self.id = id
        self._events: List[Event] = []
        self._state = OrderState()
    
    def apply_event(self, event: Event) -> None:
        self._events.append(event)
        self._state.apply(event)
    
    @property
    def version(self) -> int:
        return len(self._events)
    
    def place_order(self, items: List[OrderItem]) -> None:
        if not items:
            raise ValueError("Order must have at least one item")
        
        event = OrderPlaced(
            order_id=self.id,
            items=items,
            timestamp=datetime.now()
        )
        self.apply_event(event)
```

## Design Considerations

### Scalability
```python
# 1. Caching
from functools import lru_cache
from redis import Redis

class ProductCache:
    def __init__(self, redis: Redis):
        self._redis = redis
    
    def get_product(self, id: str) -> Optional[Product]:
        cached = self._redis.get(f"product:{id}")
        if cached:
            return Product.from_json(cached)
        return None
    
    def set_product(self, product: Product) -> None:
        self._redis.set(
            f"product:{product.id}",
            product.to_json(),
            ex=3600  # 1 hour expiry
        )

# 2. Asynchronous Processing
from asyncio import gather
from aiohttp import ClientSession

async def fetch_product_data(product_ids: List[str]) -> List[Product]:
    async with ClientSession() as session:
        tasks = [
            fetch_single_product(session, pid)
            for pid in product_ids
        ]
        return await gather(*tasks)

# 3. Load Balancing
class RoundRobinLoadBalancer:
    def __init__(self, servers: List[str]):
        self._servers = servers
        self._current = 0
    
    def get_server(self) -> str:
        server = self._servers[self._current]
        self._current = (self._current + 1) % len(self._servers)
        return server
```

### Maintainability
```python
# 1. Configuration Management
from pydantic import BaseSettings

class AppConfig(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    API_KEY: str
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"

# 2. Logging
import structlog

logger = structlog.get_logger()

class OrderService:
    def create_order(self, data: dict) -> Order:
        logger.info("creating_order", customer_id=data['customer_id'])
        try:
            order = Order.create(data)
            logger.info("order_created", order_id=str(order.id))
            return order
        except Exception as e:
            logger.error("order_creation_failed", error=str(e))
            raise

# 3. Dependency Injection
from dependency_injector import containers, providers

class Container(containers.DeclarativeContainer):
    config = providers.Singleton(AppConfig)
    
    db = providers.Singleton(
        Database,
        url=config.provided.DATABASE_URL
    )
    
    order_repository = providers.Factory(
        OrderRepository,
        session_factory=db.provided.session
    )
    
    order_service = providers.Factory(
        OrderService,
        repository=order_repository
    )
```

### Testing Strategies
```python
# 1. Integration Tests
class TestOrderCreation(IntegrationTest):
    def setUp(self):
        self.container = Container()
        self.container.config.override({
            "DATABASE_URL": "sqlite:///:memory:"
        })
        self.service = self.container.order_service()
    
    async def test_create_order(self):
        # Arrange
        customer_id = "test_customer"
        items = [{"product_id": "P1", "quantity": 1}]
        
        # Act
        order = await self.service.create_order(customer_id, items)
        
        # Assert
        assert order.id is not None
        assert order.customer_id == customer_id

# 2. Contract Tests
from pytest_bdd import scenario, given, when, then

@scenario('features/order_api.feature', 'Create new order')
def test_create_order():
    pass

@given("a valid customer")
def valid_customer():
    return {"id": "C1", "name": "Test Customer"}

@when("they place an order")
def place_order(valid_customer):
    return client.post("/orders", json={
        "customer_id": valid_customer["id"],
        "items": [{"product_id": "P1", "quantity": 1}]
    })

@then("the order should be created")
def check_order_created(place_order):
    assert place_order.status_code == 201
    assert "order_id" in place_order.json()

# 3. Load Tests
from locust import HttpUser, task, between

class OrderAPIUser(HttpUser):
    wait_time = between(1, 2)
    
    @task
    def create_order(self):
        self.client.post("/orders", json={
            "customer_id": "C1",
            "items": [{"product_id": "P1", "quantity": 1}]
        })
```

### Performance Optimization
```python
# 1. Database Optimization
class OptimizedOrderRepository:
    def get_orders_with_items(self, customer_id: str) -> List[Order]:
        return (
            self._session.query(Order)
            .options(joinedload(Order.items))  # Eager loading
            .filter(Order.customer_id == customer_id)
            .all()
        )
    
    def bulk_create_orders(self, orders: List[Order]) -> None:
        self._session.bulk_save_objects(
            [OrderModel.from_domain(order) for order in orders]
        )
        self._session.commit()

# 2. Caching Strategies
class TieredCache:
    def __init__(self, local_cache: LRUCache, redis: Redis):
        self._local = local_cache
        self._redis = redis
    
    async def get(self, key: str) -> Optional[Any]:
        # Try local cache first
        value = self._local.get(key)
        if value is not None:
            return value
        
        # Try Redis
        value = await self._redis.get(key)
        if value is not None:
            self._local.set(key, value)  # Update local cache
            return value
        
        return None

# 3. Background Tasks
from celery import Celery

app = Celery('tasks', broker='redis://localhost')

@app.task
def process_order(order_id: str) -> None:
    order = Order.get(order_id)
    order.process()
    
    # Notify other systems
    notify_shipping.delay(order_id)
    update_inventory.delay(order_id)
```

## Best Practices Summary

1. **Architecture Principles**
   - Separate concerns
   - Depend on abstractions
   - Keep components loosely coupled
   - Design for change

2. **Scalability Considerations**
   - Use caching effectively
   - Implement asynchronous processing
   - Design for horizontal scaling
   - Consider eventual consistency

3. **Maintainability Guidelines**
   - Follow consistent patterns
   - Implement proper logging
   - Use dependency injection
   - Maintain comprehensive tests

## Exercises

1. **Hexagonal Architecture**
```python
# Implement an order processing system using hexagonal architecture
# TODO: Define ports and create adapters
```

2. **Event-Driven System**
```python
# Create an event-driven order processing pipeline
# TODO: Implement events, handlers, and message bus
```

3. **Scalability Challenge**
```python
# Design a scalable product catalog system
# TODO: Implement caching and load balancing
``` 