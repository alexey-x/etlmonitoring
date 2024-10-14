import pytest
from unittest.mock import patch
from app.src.services import notify_monitoring_alive
from app.src.notify import notify
from app.src.adapters import Role


@pytest.mark.parametrize(
    "event, template, role, expected_call",
    [
        # Happy path test case
        (
            "Процесс ETL-мониторинга работает",
            "email_service_alive.j2",
            Role.ADMIN,
            True,
        ),
        # Edge case: Different event message
        ("ETL monitoring process is alive", "email_service_alive.j2", Role.ADMIN, True),
        # Edge case: Different template
        ("Процесс ETL-мониторинга работает", "different_template.j2", Role.ADMIN, True),
        # Error case: Invalid role
        (
            "Процесс ETL-мониторинга работает",
            "email_service_alive.j2",
            "INVALID_ROLE",
            False,
        ),
    ],
    ids=[
        "happy_path",
        "edge_case_different_event",
        "edge_case_different_template",
        "error_case_invalid_role",
    ],
)
def test_notify_monitoring_alive(event, template, role, expected_call):
    # Arrange
    message_param = {"event": event}

    with patch("app.src.services.notify") as mock_notify:
        # Act
        notify_monitoring_alive()

        # Assert
        if expected_call:
            mock_notify.assert_called_once_with(message_param, template, role)
        else:
            mock_notify.assert_not_called()


import pytest
from unittest.mock import patch
from app.src.services import notify_monitoring_alive
from app.src.notify import notify
from app.src.adapters import Role


@pytest.mark.parametrize(
    "event, template, role, expected_call",
    [
        # Happy path test case
        (
            "Процесс ETL-мониторинга работает",
            "email_service_alive.j2",
            Role.ADMIN,
            True,
        ),
        # Edge case: Different event message
        ("ETL monitoring process is alive", "email_service_alive.j2", Role.ADMIN, True),
        # Edge case: Different template
        ("Процесс ETL-мониторинга работает", "different_template.j2", Role.ADMIN, True),
        # Error case: Invalid role
        (
            "Процесс ETL-мониторинга работает",
            "email_service_alive.j2",
            "INVALID_ROLE",
            False,
        ),
    ],
    ids=[
        "happy_path",
        "edge_case_different_event",
        "edge_case_different_template",
        "error_case_invalid_role",
    ],
)
def test_notify_monitoring_alive(event, template, role, expected_call):
    # Arrange
    message_param = {"event": event}

    with patch("app.src.services.notify") as mock_notify:
        # Act
        notify_monitoring_alive()

        # Assert
        if expected_call:
            mock_notify.assert_called_once_with(message_param, template, role)
        else:
            mock_notify.assert_not_called()
