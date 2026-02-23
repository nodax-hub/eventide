from typing import Generic, TypeVar
from .signal import Signal

T = TypeVar("T")

class SignalDescriptor(Generic[T]):
    """
    Декларативное объявление сигнала в классе.
    """

    def __init__(self) -> None:
        self._name: str | None = None

    def __set_name__(self, owner, name) -> None:
        self._name = name

    def __get__(self, instance, owner) -> Signal[T]:
        if instance is None:
            return self  # type: ignore

        storage = instance.__dict__.setdefault("_signals", {})
        if self._name not in storage:
            storage[self._name] = Signal[T]()
        return storage[self._name]