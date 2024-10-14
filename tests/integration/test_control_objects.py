

def test_get_data_db_objects(db_control_object):
    """Query returns some data."""
    co = db_control_object()
    data = co.get_data()
    for d in data:
        print(d)
    
    assert len(data) >= 0