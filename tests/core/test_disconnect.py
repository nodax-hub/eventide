from eventide.core.signal import Signal

def test_disconnect_function():
    signal = Signal[int]()
    result = []

    def slot(value: int):
        result.append(value)

    signal.connect(slot)
    signal.disconnect(slot)
    signal.emit(1)

    assert result == []


def test_disconnect_bound_method():
    signal = Signal[int]()
    result = []

    class A:
        def slot(self, value: int):
            result.append(value)

    a = A()

    signal.connect(a.slot)
    signal.disconnect(a.slot)
    signal.emit(1)

    assert result == []