import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from app.src.stat_objects import StatScoresAlterStage
from app.src.adapters import get_settings, get_connect_db, get_sql_query
from app.src.stat_objects import StatData


@pytest.fixture
def mock_engine():
    with patch("app.src.stat_objects.get_connect_db") as mock_get_connect_db:
        mock_engine = MagicMock()
        mock_get_connect_db.return_value = mock_engine
        yield mock_engine


@pytest.fixture
def mock_query():
    with patch("app.src.stat_objects.get_sql_query") as mock_get_sql_query:
        mock_get_sql_query.return_value = "SELECT * FROM test_table"
        yield mock_get_sql_query


@pytest.fixture
def mock_settings():
    with patch("app.src.stat_objects.get_settings") as mock_get_settings:
        mock_get_settings.return_value = {}
        yield mock_get_settings


@pytest.mark.parametrize(
    "mock_data, expected_name",
    [
        (
            pd.DataFrame({"col1": [1, 2], "col2": [3, 4]}),
            "Статистика альтернативных скорров загруженных в STAGE",
        ),
        (
            pd.DataFrame({"col1": [], "col2": []}),
            "Статистика альтернативных скорров загруженных в STAGE",
        ),
    ],
    ids=["happy_path_with_data", "happy_path_empty_data"],
)
def test_get_stat_happy_path(
    mock_engine, mock_query, mock_settings, mock_data, expected_name
):
    # Arrange
    mock_engine.connect.return_value.__enter__.return_value = MagicMock()
    pd.read_sql_query = MagicMock(return_value=mock_data)
    stat_scores = StatScoresAlterStage()

    # Act
    result = stat_scores.get_stat()

    # Assert
    assert result.name == expected_name
    pd.testing.assert_frame_equal(result.data, mock_data)


@pytest.mark.parametrize(
    "mock_data",
    [
        (pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})),
    ],
    ids=["edge_case_large_data"],
)
def test_get_stat_edge_cases(mock_engine, mock_query, mock_settings, mock_data):
    # Arrange
    mock_engine.connect.return_value.__enter__.return_value = MagicMock()
    pd.read_sql_query = MagicMock(return_value=mock_data)
    stat_scores = StatScoresAlterStage()

    # Act
    result = stat_scores.get_stat()

    # Assert
    pd.testing.assert_frame_equal(result.data, mock_data)


@pytest.mark.parametrize(
    "exception",
    [
        (Exception("Database connection error")),
        (Exception("SQL query error")),
    ],
    ids=["error_case_db_connection", "error_case_sql_query"],
)
def test_get_stat_error_cases(mock_engine, mock_query, mock_settings, exception):
    # Arrange
    mock_engine.connect.side_effect = exception
    stat_scores = StatScoresAlterStage()

    # Act & Assert
    with pytest.raises(Exception) as excinfo:
        stat_scores.get_stat()
    assert str(excinfo.value) == str(exception)
