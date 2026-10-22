---
name: python-fastapi
description: FastAPI APIs with Pydantic, OpenAPI, dependencies, security, middleware, lifespan, and response models. Use for routes, validation, authentication or authorization, database-session dependencies, CORS, sync versus async handlers, pagination, errors, or startup and shutdown resources. For ORM mechanics, use python-sqlalchemy.
user-invocable: false
---

# FastAPI - Modern Python Web APIs

FastAPI is a modern, fast web framework for building APIs with Python, using standard Python type hints. FastAPI automatically validates requests, generates OpenAPI documentation, and provides excellent developer experience.

## Quick Start

### Basic Application

```python
from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI(
    title="My API",
    description="API for my application",
    version="1.0.0",
)

class CreateItem(BaseModel):
    name: str
    price: float

class Item(CreateItem):
    id: int

@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Hello World"}

@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: CreateItem) -> Item:
    return Item(id=1, **item.model_dump())
```

**Run with:**
```bash
uvicorn main:app --reload
```

## Core Concepts

### Request & Response Models

Use Pydantic models for automatic validation and serialization:

```python
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class CreateUserRequest(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=18, le=120)

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    model_config = ConfigDict(from_attributes=True)

@app.post("/users", response_model=UserResponse)
def create_user(user: CreateUserRequest) -> UserResponse:
    return UserResponse(id=1, email=str(user.email), name=user.name)
```

See `references/validation.md` for detailed validation patterns including custom validators and field constraints.

### Routers for Organization

Split routes across routers for clean organization:

```python
# routers/users.py
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
def list_users():
    ...

@router.post("/")
def create_user(user: CreateUserRequest):
    ...

# main.py
app.include_router(users.router)
```

### Dependency Injection

FastAPI's core feature for managing dependencies like database sessions and authentication:

```python
from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

def get_db() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session

DbSession = Annotated[Session, Depends(get_db)]

@app.get("/users")
def list_users(db: DbSession) -> list[User]:
    return list(db.scalars(select(User)))
```

The dependency owns cleanup only. Use application-service transaction boundaries (`with db.begin():`) for writes. Yield dependency cleanup defaults to after the response; use `Depends(get_db, scope="function")` only when cleanup must finish before it is sent.

See `references/dependencies.md` for auth, scopes, transactions, and testing overrides.

## Error Handling

### HTTP Exceptions

```python
from fastapi import HTTPException

@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

### Custom Exception Handlers

```python
from fastapi import Request
from fastapi.responses import JSONResponse

class BusinessError(Exception):
    def __init__(self, message: str):
        self.message = message

@app.exception_handler(BusinessError)
async def business_error_handler(request: Request, exc: BusinessError) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"error": exc.message},
    )
```

## Project Structure

```
my-api/
├── main.py                   # FastAPI app
├── routers/                  # Route handlers
│   ├── users.py
│   └── products.py
├── schemas/                  # Pydantic models
│   ├── users.py
│   └── products.py
├── services/                 # Business logic
│   └── users.py
├── repositories/             # Data access
│   └── users.py
└── dependencies.py           # Dependency injection
```

## Reference Materials

Detailed patterns for common scenarios:

- **Validation**: `references/validation.md` - Field constraints, custom validators, model validation
- **Dependencies**: `references/dependencies.md` - Auth services, scoped dependencies, advanced injection patterns
- **Middleware**: `references/middleware.md` - CORS, custom middleware, request/response processing
- **API Design**: `references/api-design.md` - REST naming, pagination, OpenAPI customization, status codes

## Best Practices

1. **Use validated output schemas** - A return annotation or `response_model` filters structured output; deliberately omit it for direct `Response` subclasses, files, or streams.
2. **Validate inputs** - Use Pydantic models with constraints
3. **Dependency injection** - Manage sessions, auth, and cross-cutting concerns
4. **Router organization** - Split routes by resource/domain
5. **Error handling** - Use HTTP exceptions and custom handlers appropriately
6. **Lifespan and handler choice** - Use `FastAPI(lifespan=...)` for application resources. Use `async def` only for awaited I/O; use `def` for blocking libraries.
