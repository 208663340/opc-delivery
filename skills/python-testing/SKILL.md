---
name: python-testing
description: "pytest testing for Python applications: test-first development, unit, integration, composition, and end-to-end boundaries; fixtures, mocks, fakes, async tests, and database fidelity. Use when writing or debugging tests, deciding test levels, or configuring pytest. For FastAPI or SQLAlchemy mechanics, use their dedicated skills."
user-invocable: false
---

# Testing with pytest

Test behavior at useful boundaries. The right test level depends on the contract and failure risk.

## Test-First Development

Test at component boundaries, not internal implementation:

```
HTTP adapter → application use case → domain
                         ↓
                  persistence adapter
```

Follow **test → implement → refactor**:

1. Write a focused failing behavior test.
2. Implement the smallest correct behavior.
3. Refactor while the test remains green.

```python
# Temporary skeleton, if one helps orient the code.
def calculate_discount(total: Decimal) -> Decimal:
    raise NotImplementedError

# 2. Test
def test_discount_for_large_order():
    result = calculate_discount(Decimal("150"))
    assert result == Decimal("15")

# 3. Implement
def calculate_discount(total: Decimal) -> Decimal:
    if total > 100:
        return total * Decimal("0.1")
    return Decimal("0")
```

## Layer Boundary Testing Overview

Test **what crosses layer boundaries**, not internal implementation:

- **Domain unit**: Invariants and decisions.
- **Application unit/contract**: Business workflow with a fake or autospecced collaborator.
- **Repository integration**: Real database adapter against the required dialect.
- **HTTP composition**: Validation, serialization, status codes, and dependency wiring.

See references/boundaries.md for comprehensive layer-specific examples.

## Entity Testing Example

Test business logic without framework DTOs:

```python
def test_product_apply_discount():
    """Test business logic"""
    product = Product(id=uuid4(), name="Widget", price=Decimal("100"))
    product.apply_discount(Decimal("0.1"))

    assert product.price == Decimal("90")
```

## Service Testing Example

Test orchestration with stubbed dependencies:

```python
from unittest.mock import create_autospec

def test_create_product_service():
    """Test with mocked repository"""
    mock_repo = create_autospec(ProductRepository, instance=True, spec_set=True)
    mock_repo.save.return_value = Product(id=uuid4(), name="Widget")

    service = ProductService(repo=mock_repo)
    result = service.create(CreateProductRequest(name="Widget", price=Decimal("9.99")))

    mock_repo.save.assert_called_once()
    assert result.name == "Widget"
```

## Repository Testing Example

Test the production dialect for database-specific behavior:

```python
@pytest.fixture
def test_db():
    """Fast adapter test; not a PostgreSQL fidelity test."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    yield session
    session.close()

def test_repository_save(test_db):
    """Test database operations"""
    repo = ProductRepository(test_db)
    product = Product(id=uuid4(), name="Widget", price=Decimal("9.99"))

    saved = repo.save(product)

    assert saved.id == product.id
    assert test_db.get(ProductRecord, product.id) is not None
```

## Router Testing Example

Test HTTP layer with TestClient:

```python
from fastapi.testclient import TestClient

def test_create_product_endpoint():
    """Test POST endpoint"""
    client = TestClient(app)

    response = client.post(
        "/products",
        json={"name": "Widget", "price": 9.99},
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Widget"
```

## Test Organization Basics

```
tests/
├── unit/
│   ├── test_entities.py      # Entity + Value object tests
│   └── test_services.py      # Service tests (with mocks)
├── integration/
│   ├── test_repositories.py  # Repository tests (with DB)
│   └── test_endpoints.py     # Router tests (with client)
└── conftest.py               # Shared fixtures
```

## Reference Documentation

For comprehensive patterns and examples, see:

- **references/boundaries.md** - Layer boundary testing patterns with complete examples for each layer
- **references/mocking.md** - Mock strategies, verification methods, and anti-patterns
- **references/pytest.md** - Configuration, fixtures, markers, parametrization, and debugging

## Async tests

With pytest-asyncio strict mode, mark async tests with `@pytest.mark.asyncio` and decorate async fixtures with `@pytest_asyncio.fixture`. Use `AsyncMock` and `assert_awaited_once_with` for async collaborators. See `references/pytest.md` for loop scopes and cleanup.
