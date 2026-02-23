from dataclasses import dataclass

from eventide import SignalDescriptor

@dataclass(frozen=True)
class UserRegistered:
    user_id: int

class Service:
    event = SignalDescriptor[UserRegistered]()

def test_multiple_subscribers():
    service = Service()
    calls = []

    def a(e: UserRegistered): calls.append(("a", e.user_id))
    def b(e: UserRegistered): calls.append(("b", e.user_id))

    service.event.connect(a)
    service.event.connect(b)

    service.event.emit(UserRegistered(1))

    assert calls == [("a", 1), ("b", 1)]