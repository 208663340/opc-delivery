# FastAPI Dependencies

Use `Annotated` to make dependency boundaries explicit. See the [FastAPI dependency guide](https://fastapi.tiangolo.com/tutorial/dependencies/) and [yield dependency lifecycle](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/).

## Sessions and transactions

```python
from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

def get_session() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session

DbSession = Annotated[Session, Depends(get_session)]

def create_user(data: CreateUserRequest, session: DbSession) -> UserResponse:
    with session.begin():
        user = UserModel(email=data.email, name=data.name)
        session.add(user)
    session.refresh(user)
    return UserResponse.model_validate(user)
```

Do not decorate generator dependencies with `@contextmanager`; FastAPI manages the generator itself. A class passed to `Depends` is instantiated, not entered as a context manager. A yield dependency defaults to request scope, so cleanup happens after the response. Use `scope="function"` only when cleanup must occur before sending it.

## Authentication

```python
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

bearer = HTTPBearer(auto_error=False)
Credentials = Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)]

def current_user_optional(credentials: Credentials) -> User | None:
    if credentials is None:
        return None
    try:
        return decode_and_get_user(credentials.credentials)
    except InvalidTokenError:
        return None

def current_user(credentials: Credentials) -> User:
    user = current_user_optional(credentials)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
```

Catch only the JWT library's invalid-token exception. Require and validate claims such as `sub`, `exp`, issuer, and audience when the token profile defines them. Use `Security` with declared scopes when OAuth2 scopes are part of the API contract.

Use `APIKeyHeader` and `secrets.compare_digest` for API-key schemes. Do not write raw header comparison examples that omit OpenAPI security metadata.

## Testing and lifecycle

Use `app.dependency_overrides[dependency] = replacement` in a test and clear overrides after it. Use `TestClient` as a context manager when lifespan resources need startup and shutdown.
