"""Common types used in the package."""

from enum import Enum
from contextlib import AbstractContextManager
from typing import Any, Generic, Protocol, TypeVar


class StoreValueNotExists(Exception):
    """Raised when a value is not found in the storage."""

    ...


_StoreType = TypeVar("_StoreType")


class Store(Protocol, Generic[_StoreType]):
    """Store protocol for sharing data across workers."""

    @property
    def fixtures(self) -> list[str]:
        """List of fixtures that the store needs."""
        ...

    def read(self, identifier: str, fixture_values: dict[str, Any]) -> _StoreType:
        """Read a value from the storage.

        Raises:
            StoreValueNotExists: If the identifier is not found in the storage.
        """
        ...

    def write(self, identifier: str, data: _StoreType, fixture_values: dict[str, Any]):
        """Write a value to the storage."""
        ...

    def lock(self, identifier: str, fixture_values: dict[str, Any]) -> AbstractContextManager:
        """Lock to ensure atomicity."""
        ...


class CleanupToken(str, Enum):
    """Token that is send back to the fixture after last yield."""

    LAST = "last"
