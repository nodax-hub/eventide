import gc
from eventide.core.signal import Signal

def test_slot_garbage_collected():
    signal = Signal[int]()
    result = []

    class A:
        def slot(self, value: int):
            result.append(value)

    a = A()
    signal.connect(a.slot)

    del a
    gc.collect()

    signal.emit(1)

    assert result == []