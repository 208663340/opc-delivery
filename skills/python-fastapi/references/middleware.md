# FastAPI and Starlette Middleware

Use middleware for transport-wide concerns such as correlation IDs, compression, trusted hosts, and CORS. Prefer dependencies for authorization and application services for transactions. Read the [Starlette middleware documentation](https://www.starlette.io/middleware/) for ordering and limitations.

## CORS

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH"],
    allow_headers=["Authorization", "Content-Type"],
)
```

When credentials are enabled, enumerate origins, methods, and headers. A wildcard origin is acceptable only for intentionally non-credentialed access with `allow_credentials=False`. Wrap the whole application with CORS middleware when error responses must also carry CORS headers.

## Custom middleware

Function-style middleware is appropriate for small application-local logic:

```python
from time import perf_counter

from fastapi import Request

@app.middleware("http")
async def timing(request: Request, call_next):
    start = perf_counter()
    response = await call_next(request)
    response.headers["X-Process-Time"] = str(perf_counter() - start)
    return response
```

Use pure ASGI middleware for reusable infrastructure, streaming/body work, or `ContextVar`-sensitive behavior. `BaseHTTPMiddleware` has documented `ContextVar` propagation limitations and is not merely a slower equivalent.

## Error handling and security

Let unexpected errors propagate to centralized logging and exception handling. Log a correlation ID server-side; return a stable generic error response, never `str(exc)` or tracebacks. Use RFC 9457 `application/problem+json` if adopting Problem Details.

An in-process IP dictionary is a demonstration only, not production rate limiting. Production limits need a shared atomic store or gateway, bounded TTL keys, authenticated-principal and endpoint policies, and trusted-proxy configuration.

Do not commit database sessions in middleware. Handled HTTP errors and streaming responses make request-wide transaction middleware unsafe; scope transactions at the application use case instead.

Do not use `X-XSS-Protection`. Prefer output encoding, Content Security Policy, `X-Content-Type-Options: nosniff`, and appropriate `frame-ancestors` policy.
