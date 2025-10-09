import pytest

from app.src.adapters import get_connect_db, get_settings
from app.src.stat_objects import select_alter_score_table_names

from app.src.stat_objects import (
    StatScoresMO,
    StatScoresAlterMO,
    StatLTVMO,
)

@pytest.fixture(
    params=[
        StatScoresMO,
        StatScoresAlterMO,
        StatLTVMO,
    ]
)
def stat_object(request):
    """Provide classes for all stat objects."""
    return request.param


def test_select_alter_score_table_names():
    database = "modb"
    engine = get_connect_db(database, get_settings())
    prefix = "SCORE_MODEL_RESULTS_ALTER"
    alter_scores_tables = select_alter_score_table_names(engine)
    assert all(prefix in table for table in alter_scores_tables)





# def test_get_stat(stat_object):
#     """Query returns some statistical data."""
#     stat = stat_object()
#     data = stat.get_stat()
#     print(data)
    
#     assert hasattr(data, "data_name")
#     assert hasattr(data, "data_table")
