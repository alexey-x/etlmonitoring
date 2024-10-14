
from unittest.mock import patch, Mock

from app.src.stat_objects import  (
    select_alter_score_tables_with_max_date,
    select_alter_score_table_names,
    StatScoresAlterMO,
)


def test_select_alter_score_tables_with_max_date():
    score_tables = [
        "INTEGRATION.SCORE_MODEL_RESULTS_ALTER_20240826170221_3",
        "INTEGRATION.SCORE_MODEL_RESULTS_ALTER_20240826170221_2",
        "INTEGRATION.SCORE_MODEL_RESULTS_ALTER_20240826170221_1",
        "INTEGRATION.SCORE_MODEL_RESULTS_ALTER_20240807105525_1",
        "INTEGRATION.SCORE_MODEL_RESULTS_ALTER_20240807105525_0",
    ]
    max_date = "20240826170221"
    scores_with_max_date = [t for t in score_tables if max_date in t]
    assert scores_with_max_date == select_alter_score_tables_with_max_date(score_tables)

def test_select_alter_score_tables_with_max_date_date_empty_list():
    assert [] == select_alter_score_tables_with_max_date([])

def test_select_alter_score_tables_with_max_date_no_match():
    score_tables = [
        "INTEGRATION.SCORE_MODEL_RESULTS_ALTER_xxx",
        "INTEGRATION.SCORE_MODEL_RESULTS_ALTER_yyy",
    ]
    assert [] == select_alter_score_tables_with_max_date(score_tables)

# @patch("sqlalchemy.engine.Engine")
# def test_select_alter_score_table_names(mock_engine):
#     conn = mock_engine.return_value.__enter__.return_value
#     cursor = Mock()
#     conn.execute.return_value = cursor
#     # conn.cursor.fetchall.return_value = [("table1",), ("table2",)]
#     out = select_alter_score_table_names(mock_engine)
#     assert conn.execute.assert_called_once()
#     result = ["table1", "table2"]
#     # assert result == out

def test_StatScoresAlterMO_make_query_to_all_tables():
    so = StatScoresAlterMO()
    all_tables = ["table1", "table2", "table3"]
    query = [f"select * from {table} " for table in all_tables]
    query = "union all\n".join(query)
    assert query in so._make_query_to_all_tables(all_tables)

