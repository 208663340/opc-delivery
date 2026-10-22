# Test Doubles

Use the smallest double that preserves the contract:

- Dummy: fills an unused parameter.
- Stub: returns canned indirect inputs.
- Fake: simplified working implementation.
- Spy or mock: records interactions.

Prefer state/output assertions. Verify interactions only when call count, ordering, or arguments are contractual. Use autospec to catch spelling and signature drift.

```python
from unittest.mock import create_autospec

repo = create_autospec(UserRepository, instance=True, spec_set=True)
repo.get.return_value = user
```

Use `AsyncMock` for async callables and `assert_awaited_once_with`, not `assert_called_once_with`. `MagicMock` is for magic methods such as context managers and iteration; ordinary `Mock` also supports chained child mocks.

Patch the name where the system under test looks it up, for example `myapp.notifications.requests.post`, not necessarily `requests.post`. Prefer dependency injection when practical.
