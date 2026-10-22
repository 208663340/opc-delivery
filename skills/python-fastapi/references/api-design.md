# FastAPI API Design

Use resource-oriented names when they clarify the contract, but prioritize domain language and client needs. `POST /products/{product_id}/reviews` creates a server-identified review; client-selected resource identifiers normally use `PUT`.

`PUT` is idempotent. `PATCH` is neither safe nor inherently idempotent; a particular patch document can be designed to be idempotent. Apply patches atomically and use conditional requests such as `If-Match` where concurrent updates matter.

## Problem Details

RFC 9457 supersedes RFC 7807. If using Problem Details, set its media type explicitly and do not expose internal exception text.

```python
from fastapi.responses import JSONResponse

def problem(status: int, title: str, detail: str) -> JSONResponse:
    return JSONResponse(
        status_code=status,
        media_type="application/problem+json",
        content={"type": "about:blank", "title": title, "status": status, "detail": detail},
    )
```

## Pagination and idempotency

Paginated queries require deterministic ordering. For deep lists, use a unique composite key such as `(created_at, id)`, a matching lexicographic predicate, and an opaque authenticated cursor. Use `is not None` for optional numeric filters so zero is retained.

An idempotency key needs a database uniqueness constraint scoped to caller and operation, a request fingerprint, an in-progress policy, and a stored replayable response in the same transaction. A prior `SELECT` followed by `INSERT` is race-prone.

Use a generic `Page[T]` response model so OpenAPI and clients retain item typing. See the [FastAPI response model guide](https://fastapi.tiangolo.com/tutorial/response-model/).
