import weakref
from typing import Callable, Generic, TypeVar, Optional

from .errors import ErrorPolicy
from .types import Slot

T = TypeVar("T")


class _SlotRef:
    def __init__(self, slot: Callable):
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
    def __init__(
            self,
            *,
            error_policy: ErrorPolicy = ErrorPolicy.FAIL_FAST,
            on_error: Optional[Callable[[Exception, Callable], None]] = None,
    ) -> None:
        self._slots: list[_SlotRef] = []
        self._error_policy = error_policy
        self._on_error = on_error

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
            if fn is None:
                continue

            try:
                fn(event)
                alive.append(ref)
            except Exception as exc:
                if self._on_error is not None:
                    self._on_error(exc, fn)

                if self._error_policy is ErrorPolicy.FAIL_FAST:
                    raise

                # ISOLATE → продолжаем

        self._slots = alive
