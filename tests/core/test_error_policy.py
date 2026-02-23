import pytest
from eventide.core.signal import Signal
from eventide.core.errors import ErrorPolicy


def test_fail_fast_stops_emit():
    signal = Signal[int](error_policy=ErrorPolicy.FAIL_FAST)
    calls = []

    def bad(_: int):
        raise RuntimeError("boom")

    def good(_: int):
        calls.append("good")

    signal.connect(bad)
    signal.connect(good)

    with pytest.raises(RuntimeError):
        signal.emit(1)

    assert calls == []


def test_isolate_continues_emit():
    signal = Signal[int](error_policy=ErrorPolicy.ISOLATE)
    calls = []

    def bad(_: int):
        raise RuntimeError("boom")

    def good(_: int):
        calls.append("good")

    signal.connect(bad)
    signal.connect(good)

    signal.emit(1)

    assert calls == ["good"]


def test_on_error_called():
    errors = []

    def on_error(exc: Exception, slot):
        errors.append((type(exc), slot))

    signal = Signal[int](
        error_policy=ErrorPolicy.ISOLATE,
        on_error=on_error,
    )

    def bad(_: int):
        raise ValueError("fail")

    signal.connect(bad)
    signal.emit(1)

    assert len(errors) == 1
    assert errors[0][0] is ValueError