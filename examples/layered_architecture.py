from dataclasses import dataclass

from eventide import SignalDescriptor


@dataclass(frozen=True)
class UserRegistered:
    user_id: int


class UserService:
    registered = SignalDescriptor[UserRegistered]()

    def register(self, user_id: int) -> None:
        print("UserService: register")
        self.registered.emit(UserRegistered(user_id))


def send_email(event: UserRegistered) -> None:
    print(f"Email sent to user {event.user_id}")


def write_audit_log(event: UserRegistered) -> None:
    print(f"Audit: user {event.user_id} registered")


service = UserService()

service.registered.connect(send_email)
service.registered.connect(write_audit_log)

service.register(7)