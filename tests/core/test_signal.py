from eventide.core.signal import Signal

def test_signal_calls_slot():
    signal = Signal[int]()
    result = []

    def slot(value: int) -> None:
        result.append(value)

    signal.connect(slot)
    signal.emit(10)

    assert result == [10]