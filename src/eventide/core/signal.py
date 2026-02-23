import weakref
from typing import Callable, Generic, TypeVar

T = TypeVar("T")

class Signal(Generic[T]):
    """
    Runtime signal.
    Хранит weak-ссылки на слоты.
    """

    def __init__(self) -> None:
        self._slots: list[weakref.ReferenceType] = []

    def connect(self, slot: Callable[[T], None]) -> None:
        self._slots.append(weakref.ref(slot))

    def emit(self, event: T) -> None:
        alive: list[weakref.ReferenceType] = []
        for ref in self._slots:
            fn = ref()
            if fn is not None:
                fn(event)
                alive.append(ref)
        self._slots = alive