from dataclasses import dataclass

from eventide.core.descriptor import SignalDescriptor

@dataclass(frozen=True)
class DataReady:
    value: int

class A:
    sig = SignalDescriptor[DataReady]()

def test_descriptor_is_instance_bound():
    a1 = A()
    a2 = A()

    assert a1.sig is not a2.sig