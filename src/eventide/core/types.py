from typing import Protocol, TypeVar

T = TypeVar("T")

class Slot(Protocol[T]):
    def __call__(self, event: T) -> None: ...