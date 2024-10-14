import jinja2
import datetime


from app.src.control_objects import (
    SegmentMODB,
)

from app.src.adapters import (
    get_email_template,
)

TEXT = """
<div>{{event}}</div>

<div>{{par[0].event}}, {{par[0].attr}}</div>

<div>{{par[1].event}}, {{par[1].attr}}</div>
"""

class MSG:
    def __init__(self, event, attr) -> None:
        self.event = event
        self.attr = attr


def get_template(txt: str) -> jinja2.Template:
    env = jinja2.Environment()
    return env.from_string(txt)


def test_render_template():
    m1 = MSG("ok", "ok-attr")
    m2 = MSG("bad", "bad-attr")
    context = {"par": [m1, m2], "event": "test"}
    tmpl = get_template(TEXT)
    msg = tmpl.render(context)

    print(msg)

class FakeTabMOSegments:
    def __init__(self, segment_cd: str, count: int, created_dttm: datetime.datetime) -> None:
        self.segment_cd = segment_cd
        self.count = count
        self.created_dttm = created_dttm

def test_SegmentMODB():
    segment = SegmentMODB()
    template = get_email_template(segment.message_template)
    data = [
        FakeTabMOSegments("FakeSegment", 1, datetime.datetime.now())
    ]
    message_param = {
            "event": segment.event,
            "data": data
        }

    print(template.render(message_param))     