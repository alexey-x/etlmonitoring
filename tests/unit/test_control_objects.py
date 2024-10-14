from unittest.mock import patch

from app.src.adapters import (
    SQL_QUERIES,
)

def test_database_control_object_attributes(db_control_object):
    """Is it change code detector?"""
    assert hasattr(db_control_object, "event")
    assert hasattr(db_control_object, "database")
    assert hasattr(db_control_object, "sql")
    assert hasattr(db_control_object, "model")
    assert hasattr(db_control_object, "message_template")


def test_sql_file_exists(db_control_object):
    co = db_control_object()
    assert (SQL_QUERIES / co.sql).is_file()


def test_get_data_exists(db_control_object):
    co = db_control_object
    with patch.object(co, "get_data", autospec=True) as mock_get_data:
        co_mock = co()
        co_mock.get_data()
    mock_get_data.assert_called_once()

