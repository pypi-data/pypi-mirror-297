from typing import Callable, Optional, TypeVar

T = TypeVar("T")


def unwrap(value: Optional[T], default: Optional[T] = None) -> T:
    """Unwrap a value, or return a default if the value is None."""
    if value is not None:
        return value
    if default is not None:
        return default
    raise ValueError("value is None")


def unwrap_or_else(value: Optional[T], default: Callable[[], T]) -> T:
    """Unwrap a value, or create a default from a function if the value is None."""
    if value is not None:
        return value
    return default()


def expect(value: Optional[T], message: str) -> T:
    """Raise an exception if the value is None."""
    if value is None:
        raise ValueError(message)
    return value
