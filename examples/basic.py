from dataclasses import dataclass

from eventide import SignalDescriptor


@dataclass(frozen=True)
class DataReady:
    value: int


class Producer:
    data_ready = SignalDescriptor[DataReady]()

    def work(self) -> None:
        self.data_ready.emit(DataReady(value=42))


def handler(event: DataReady) -> None:
    print(event.value)


p = Producer()
p.data_ready.connect(handler)
p.work()
