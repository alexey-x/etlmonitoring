import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session
from app.src.control_objects import SegmentMODB
from app.src.model import TabMOSegments
from app.src.notify import notify
from app.src.stat_objects import calc_stat


@pytest.fixture
def mock_get_connect_db():
    with patch("app.src.control_objects.get_connect_db") as mock:
        yield mock


@pytest.fixture
def mock_get_sql_query():
    with patch("app.src.control_objects.get_sql_query") as mock:
        yield mock


@pytest.fixture
def mock_get_session():
    with patch("app.src.control_objects.get_session") as mock:
        yield mock


@pytest.fixture
def mock_notify():
    with patch("app.src.control_objects.notify") as mock:
        yield mock


@pytest.fixture
def mock_calc_stat():
    with patch("app.src.control_objects.calc_stat") as mock:
        yield mock


@pytest.mark.parametrize(
    "query_result, expected_data",
    [
        ([TabMOSegments()], [TabMOSegments()]),  # happy path
        ([], []),  # edge case: no data
    ],
    ids=["single_segment", "no_data"],
)
def test_get_data(
    mock_get_connect_db,
    mock_get_sql_query,
    mock_get_session,
    query_result,
    expected_data,
):
    # Arrange
    mock_session = MagicMock(spec=Session)
    mock_session.query().from_statement().all.return_value = query_result
    mock_get_session.return_value.__enter__.return_value = mock_session

    segment_modb = SegmentMODB()

    # Act
    result = segment_modb.get_data()

    # Assert
    assert result == expected_data


@pytest.mark.parametrize(
    "data, stat_result",
    [
        ([TabMOSegments()], {"stat_key": "stat_value"}),  # happy path
        ([], {"stat_key": "stat_value"}),  # edge case: no data
    ],
    ids=["single_segment", "no_data"],
)
def test_process_data(mock_notify, mock_calc_stat, data, stat_result):
    # Arrange
    mock_calc_stat.return_value = stat_result
    segment_modb = SegmentMODB()

    # Act
    segment_modb.process_data(data)

    # Assert
    mock_notify.assert_called_once()
    args, kwargs = mock_notify.call_args
    assert args[0]["event"] == segment_modb.event
    assert args[0]["data"] == data
    assert args[0]["stat"] == stat_result
    assert args[1] == segment_modb.message_template
    assert args[2] == Role.USER


def test_init(mock_get_connect_db, mock_get_sql_query):
    # Act
    segment_modb = SegmentMODB()

    # Assert
    mock_get_connect_db.assert_called_once_with(segment_modb.database, get_settings())
    mock_get_sql_query.assert_called_once_with(segment_modb.sql)
