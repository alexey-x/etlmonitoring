from app.src.notify import notify
from app.src.adapters import Role


def notify_monitoring_alive() -> None:
    message_param = {"event": "Процесс ETL-мониторинга работает"}
    notify(message_param, "email_service_alive.j2", Role.ADMIN)


def notify_admin(event: str, data: str) -> None:
    notify(
        message_param={"event": event, "data": data},
        message_template="email_error.j2",
        role=Role.ADMIN,
    )
