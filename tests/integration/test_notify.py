import datetime
from app.src.notify import notify

def test_notify(provide_FakeTabMOSegments):
    # WARNING: bad test - never fails because notify catches all exeptions
    message_template = "email_co_SegmentMODB.j2"
    data = [
        provide_FakeTabMOSegments("FakeSegment-1", 1, datetime.datetime.now()),
        provide_FakeTabMOSegments("FakeSegment-2", 2, datetime.datetime.now()),

    ]
    message_param = {
        "event": "fake-event",
        "data": data
    }        
    notify(message_param, message_template)

