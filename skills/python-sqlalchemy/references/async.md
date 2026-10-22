# Async SQLAlchemy

Read the [asyncio extension documentation](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html) before using async ORM code.

```python
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/db")
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        yield session
```

`AsyncSession` is mutable transaction state. Create one session per concurrent task; never share it through `asyncio.gather()`.

```python
from sqlalchemy import select
from sqlalchemy.orm import selectinload

async def list_users(session: AsyncSession) -> list[User]:
    return list(
        await session.scalars(
            select(User).options(selectinload(User.orders)).order_by(User.id)
        )
    )

async def create_user(session: AsyncSession, user: User) -> None:
    async with session.begin():
        session.add(user)
```

Avoid implicit lazy-loading I/O in async code. Prefer `selectinload()`, explicit `refresh()`, `lazy="raise"`, or `AsyncAttrs.awaitable_attrs`. Dispose a non-application-global engine with `await engine.dispose()` when its event loop is ending.
