import weakref
from typing import Callable
from typing import Generic, TypeVar

from .types import Slot

T = TypeVar("T")


class _SlotRef:
    """
    Унифицированная weak-ссылка на слот:
    - function
    - bound method (instance + function)
    """

    def __init__(self, slot: Callable):
        # bound method
        if hasattr(slot, "__self__") and hasattr(slot, "__func__"):
            self._is_method = True
            self._self_ref = weakref.ref(slot.__self__)
            self._func = slot.__func__
        else:
            self._is_method = False
            self._ref = weakref.ref(slot)

    def get(self):
        if self._is_method:
            instance = self._self_ref()
            if instance is None:
                return None
            return self._func.__get__(instance)
        else:
            return self._ref()

    def matches(self, slot: Callable) -> bool:
        if self._is_method:
            return (
                    hasattr(slot, "__self__")
                    and hasattr(slot, "__func__")
                    and self._self_ref() is slot.__self__
                    and self._func is slot.__func__
            )
        else:
            return self._ref() is slot


class Signal(Generic[T]):
    """
    Runtime signal.
    Хранит weak-ссылки на слоты.
    """

    def __init__(self) -> None:
        self._slots: list[_SlotRef] = []

    def connect(self, slot: Slot[T]) -> None:
        self._slots.append(_SlotRef(slot))

    def disconnect(self, slot: Slot[T]) -> None:
        self._slots = [
            ref for ref in self._slots
            if not ref.matches(slot)
        ]

    def emit(self, event: T) -> None:
        alive: list[_SlotRef] = []

        for ref in self._slots:
            fn = ref.get()
            if fn is not None:
                fn(event)
                alive.append(ref)

        self._slots = alive
