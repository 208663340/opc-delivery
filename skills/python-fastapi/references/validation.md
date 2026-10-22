# Pydantic Validation in FastAPI

Pydantic validates boundary shape; domain code must still enforce business invariants. It is coercive by default and ignores unknown fields by default, so choose strictness and extras deliberately. See the [Pydantic validation documentation](https://docs.pydantic.dev/latest/concepts/validators/).

```python
from datetime import datetime, timezone
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, StringConstraints

Username = Annotated[str, StringConstraints(min_length=3, max_length=50)]

class CreateUser(BaseModel):
    model_config = ConfigDict(extra="forbid")

    username: Username
    email: EmailStr
    age: Annotated[int, Field(ge=18, le=120)]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
```

`constr()` and `conint()` still work but are discouraged in Pydantic v2 because their dynamic types are less friendly to static tooling and are planned for deprecation. Use `EmailStr` instead of a hand-written email regex; install `email-validator` through the Pydantic email extra. `decimal_places=2` means at most two decimal places, not exactly two.

Use before, after, plain, or wrap validators according to the value stage required. An after field validator does not run when a preceding `Field(ge=...)` constraint already rejects the value.
