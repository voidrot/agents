# Python Patterns — Detailed Idiom Reference

## Core Idioms

- **Readability counts**: prefer clear names and direct control flow.
- **Explicit is better than implicit**: avoid hidden side effects and magic imports.
- **EAFP**: catch specific exceptions where attempting the operation is clearer than pre-checking every condition.
- **Type hints**: document public function contracts with modern built-in generics (`list[str]`, `dict[str, int]`) when supported.
- **Protocols**: use structural typing when callers only need a small behavior contract.

## Typing Patterns

```python
from typing import Any, Protocol, TypeAlias, TypeVar

JSON: TypeAlias = dict[str, Any] | list[Any] | str | int | float | bool | None
T = TypeVar("T")

class Renderable(Protocol):
    def render(self) -> str: ...

def first(items: list[T]) -> T | None:
    return items[0] if items else None
```

## Error Handling

```python
class ConfigError(Exception):
    """Raised when configuration cannot be loaded."""


def load_config(path: str) -> Config:
    try:
        return Config.from_path(path)
    except FileNotFoundError as exc:
        raise ConfigError(f"Config file not found: {path}") from exc
```

Guidelines:

- Catch specific exceptions.
- Avoid bare `except` and silent failure.
- Preserve cause with `raise ... from ...`.
- Keep exception classes domain-specific when callers need to branch on them.

## Context Managers

Use `with` for resource lifetime and `contextlib.contextmanager` for small custom scopes.

```python
from contextlib import contextmanager
from time import perf_counter

@contextmanager
def timer(name: str):
    start = perf_counter()
    yield
    print(f"{name} took {perf_counter() - start:.4f}s")
```

## Comprehensions and Generators

Use comprehensions for simple transformations; expand complex logic into named loops or generator functions.

```python
names = [user.name for user in users if user.is_active]

def read_lines(path: str):
    with open(path) as file:
        for line in file:
            yield line.strip()
```

## Data Containers

Use `@dataclass` for plain data with generated methods. Put invariants in `__post_init__` when construction must validate input.

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class User:
    id: str
    email: str
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        if "@" not in self.email:
            raise ValueError(f"Invalid email: {self.email}")
```

## Decorators

Use `functools.wraps` so decorated functions keep metadata.

```python
import functools
from collections.abc import Callable

def logged(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
```

## Package Organization

- Prefer `src/` layout for installable packages.
- Keep import order: standard library, third-party, local.
- Export deliberate public API from `__init__.py`; avoid wildcard imports.
- Use `ruff`/`isort`/formatter rather than hand-sorting large import blocks.

## Lightweight Performance Idioms

- Use generators for large or streaming data.
- Use `"".join(parts)` or `io.StringIO` for repeated string building.
- Consider `__slots__` only for many instances on memory-sensitive paths.
- Move async/concurrency choices to `async-python-patterns`.

## Anti-Patterns to Avoid

```python
# Mutable default

def append_to(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

# Precise None comparison
if value is None:
    handle_missing()

# Specific exception
try:
    risky_operation()
except SpecificError as exc:
    logger.warning("Operation failed: %s", exc)
```
