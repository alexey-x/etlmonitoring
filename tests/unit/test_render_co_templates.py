import pandas as pd

from app.src.adapters import (
    get_email_template,
)

from app.src.stat_objects import StatData
from app.src.control_objects import ScoreAltScoreLTV

DF = pd.DataFrame({"COL1": [1000], "COL2": [0.00000000001]})


def test_db_control_object_templates(db_control_object):
    co = db_control_object()
    template = get_email_template(co.message_template)
    message_param = {
            "event": co.event,
            "data": [],
            "stat": []
        }
    print(template.render(message_param))

def test_co_template():
    event = "Test template"
    data = []
    stat = StatData("Stat-Data-Name", DF)
    co = ScoreAltScoreLTV()
    stat = StatData("Stat-Data-Name", DF)
    template = get_email_template(co.message_template)
    message_param = {
            "event": co.event,
            "data": [],
            "stat": [stat]
        }
    print(template.render(message_param))