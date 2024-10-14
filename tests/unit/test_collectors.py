import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


from unittest.mock import patch, Mock
from typing import Iterable, List

from app.src.collectors import (
    Collector,
)
from app.src.model import (
    TabMAProcessLoadStatus,
    Base,
)
from app.src.adapters import (
    logger,
)

from app.src.control_objects import ControlObject


def test_collect():
    class ControlObject:
        pass

    class Logger:
        pass

    with patch.object(
        Collector, "collect", return_value=None, autospec=True
    ) as mock_collect:
        Collector(ControlObject, Logger())
    mock_collect.assert_called_once()


@pytest.fixture()
def db_session() -> Session:
    engine = create_engine("sqlite:///:memory:", echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(bind=engine)
    yield session
    session.close()


@pytest.fixture()
def fake_object(db_session):
    class FakeControlObject:
        model = TabMAProcessLoadStatus

        def __init__(self) -> None:
            self.session = db_session
            # self.query =

        def get_data(self) -> List[TabMAProcessLoadStatus]:
            return self.session.query(self.model).all()

        def notify(self, data: Iterable) -> None:
            pass

    return FakeControlObject


def test_TabMAProcessLoadStatus_dbwork(fake_object, db_session):
    co = Collector(fake_object, logger)

    assert len(co.tracing_data) == 0

    row = TabMAProcessLoadStatus(
        process_name="offers_transfer", load_id=1, status="new"
    )
    db_session.add(row)
    db_session.commit()
    print("\n----")
    print(db_session.query(TabMAProcessLoadStatus).all())

    co.tracing_data = co.collect()
    print(co.tracing_data)

    assert len(co.tracing_data) == 1
    # update
    row.status = "success"
    db_session.commit()
    print(db_session.query(TabMAProcessLoadStatus).all())


@pytest.fixture
def mock_logger():
    return Mock()


@pytest.fixture
def mock_control_object():
    return Mock(spec=ControlObject)


@pytest.mark.parametrize(
    "data, expected_result",
    [
        (["data1", "data2"], {"data1", "data2"}, "happy path with two items"),
        ([], set(), "happy path with no items"),
        (None, set(), "edge case with None data"),
    ],
    ids=lambda x: x[2],
)
def test_collect_new(mock_control_object, mock_logger, data, expected_result):
    # Arrange
    mock_control_object.get_data.return_value = data
    collector = Collector(mock_control_object, mock_logger)

    # Act
    result = collector.collect()

    # Assert
    assert result == expected_result


@pytest.mark.parametrize(
    "initial_data, new_data, expected_diff",
    [
        ({"data1"}, {"data1", "data2"}, {"data2"}, "new data with one new item"),
        ({"data1", "data2"}, {"data1", "data2"}, set(), "no new data"),
        (set(), {"data1"}, {"data1"}, "new data from empty initial"),
    ],
    ids=lambda x: x[3],
)
def test_check_new(
    mock_control_object, mock_logger, initial_data, new_data, expected_diff
):
    # Arrange
    mock_control_object.get_data.side_effect = [initial_data, new_data]
    collector = Collector(mock_control_object, mock_logger)

    # Act
    collector.check_new()

    # Assert
    if expected_diff:
        mock_control_object.process_data.assert_called_once_with(expected_diff)
    else:
        mock_control_object.process_data.assert_not_called()


@pytest.mark.parametrize(
    "exception, log_message",
    [
        (TypeError, "got None from database - no connection"),
        (Exception("test error"), "collect error reason: test error"),
    ],
    ids=lambda x: x[1],
)
def test_collect_exceptions(mock_control_object, mock_logger, exception, log_message):
    # Arrange
    mock_control_object.get_data.side_effect = exception
    collector = Collector(mock_control_object, mock_logger)

    # Act
    with patch("app.src.collectors.notify_admin") as mock_notify_admin:
        result = collector.collect()

    # Assert
    assert result == set()
    mock_logger.warning.assert_any_call(log_message)
    if isinstance(exception, Exception):
        mock_notify_admin.assert_called_once()


@pytest.mark.parametrize(
    "exception, log_message",
    [
        (Exception("test error"), "check error reason: test error"),
    ],
    ids=lambda x: x[1],
)
def test_check_new_exceptions(mock_control_object, mock_logger, exception, log_message):
    # Arrange
    mock_control_object.get_data.side_effect = [{"data1"}, {"data1", "data2"}]
    mock_control_object.process_data.side_effect = exception
    collector = Collector(mock_control_object, mock_logger)

    # Act
    with patch("app.src.collectors.notify_admin") as mock_notify_admin:
        collector.check_new()

    # Assert
    mock_logger.error.assert_any_call(log_message)
    mock_notify_admin.assert_called_once()
