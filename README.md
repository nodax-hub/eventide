Eventide — минималистичная typed signal/event система
в духе Qt Signals/Slots.

Принципы:
- события объявляются в классе
- отправитель не знает подписчиков
- сигнатура события = тип данных
- zero dependencies

Не предоставляет:
- async
- threading
- persistence