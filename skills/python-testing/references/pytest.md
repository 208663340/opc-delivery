# pytest and pytest-asyncio

Use `conftest.py` for auto-discovered shared fixtures and `yield` fixtures for teardown. Do not share an ORM `Session` across a test session; share only immutable or expensive infrastructure and isolate test state.

For new pytest 9 projects, native `[tool.pytest]` TOML and `strict = true` are available. Keep `[tool.pytest.ini_options]` when compatibility requires it. Attribute plugin options such as `--cov`, `--html`, `--json-report`, and `-n` to their plugins.

pytest-asyncio defaults to strict mode. In strict mode, mark tests and use its fixture decorator:

```python
import pytest
import pytest_asyncio

@pytest_asyncio.fixture
async def client() -> AsyncClient:
    async with make_client() as value:
        yield value

@pytest.mark.asyncio
async def test_fetch(client: AsyncClient) -> None:
    assert await client.fetch() == "ok"
```

Configure `asyncio_mode`, `asyncio_default_fixture_loop_scope`, and `asyncio_default_test_loop_scope` explicitly. The old `event_loop` fixture is removed and marker `scope=` is obsolete; use `loop_scope=`. Loop scope must be at least as broad as fixture caching scope.

`pytest.raises(..., match=...)` uses regular-expression search. Add a reason and normally `strict=True` to `xfail` so unexpected passes are surfaced.
