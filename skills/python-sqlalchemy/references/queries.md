# SQLAlchemy 2.0 Queries

Use `select()` with `Session.scalars()`, `Session.scalar()`, or `Session.execute()`. The [2.0 query guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html) is authoritative.

```python
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

user = session.get(User, user_id)
active_users = session.scalars(select(User).where(User.is_active)).all()
count = session.scalar(select(func.count()).select_from(User))

# scalar_one() raises for zero or multiple rows; use only when that is the contract.
user = session.scalar(select(User).where(User.email == email))

users = session.scalars(
    select(User)
    .options(selectinload(User.orders))
    .order_by(User.id)
).all()
```

`join()` filters rows; it does not populate a relationship. Collection joins can duplicate parent identities. When using `joinedload()` on a collection, call `.unique()` before consuming the result.

```python
from sqlalchemy.orm import joinedload

users = session.scalars(
    select(User).options(joinedload(User.orders)).order_by(User.id)
).unique().all()
```

Always specify a deterministic `order_by()` for pagination. `LIMIT/OFFSET` is suitable for shallow pages; use keyset pagination with a unique tie-breaker for large or deep lists. Do not call `.all()` for unbounded API or batch results; paginate or use `yield_per`/streaming.
