import datetime

from app.src.model import (
    TabMAProcessLoadStatus,
    TabScenario,
    TabMOOffersAgg,
    TabMOSegments,
    TabETLHDP_LoadCalendar,

)

def test_TabScenario_hashable():
    s1 = TabScenario(scenario_id=1, scenario_nm="scenario1")
    s2 = TabScenario(scenario_id=1, scenario_nm="scenario1")
    s3 = TabScenario(scenario_id=2, scenario_nm="scenario2")

    assert hash(s1) == hash(1)
    assert len(set([s1])) == 1
    assert len(set([s1, s2])) == 1
    assert len(set([s1, s2, s3])) == 2

def test_TabMOOffers_hashable():
    s1 = TabMOOffersAgg(segment_cd=1, status="new")
    s2 = TabMOOffersAgg(segment_cd=1, status="new")
    s3 = TabMOOffersAgg(segment_cd=1, status="new", created_dttm=datetime.datetime.now())
    s4 = TabMOOffersAgg(segment_cd=2, status="any")

    assert hash(s1) == hash((1, "new", None, None))
    assert len(set([s1])) == 1
    assert len(set([s1, s2])) == 1
    assert s1 != s3
    assert len(set([s1, s2, s4])) == 2


def test_TabMOSegments_hashable():
    s1 = TabMOSegments(segment_cd="segment_1")
    s2 = TabMOSegments(segment_cd="segment_1")
    s3 = TabMOSegments(segment_cd="segment_2")

    assert hash(s1) == hash("segment_1")
    assert len(set([s1])) == 1
    assert len(set([s1, s2])) == 1
    assert len(set([s1, s2, s3])) == 2

def test_TabMAProcessLoadStatus_hashable():
    s1 = TabMAProcessLoadStatus(process_name="offers_transfer", load_id=1, status="some-status")
    s2 = TabMAProcessLoadStatus(process_name="offers_transfer", load_id=1, status="some-status")
    s3 = TabMAProcessLoadStatus(process_name="offers_transfer", load_id=2, status="new-status")

    assert hash(s1) == hash(("offers_transfer", 1, "some-status"))
    assert len(set([s1])) == 1
    assert len(set([s1, s2])) == 1
    assert len(set([s1, s2, s3])) == 2

def test_TabMAProcessLoadStatus_none_hashable():
    s1 = TabMAProcessLoadStatus(process_name="offers_transfer", load_id=None, status=None)
    assert hash(s1) == hash(("offers_transfer", None, None))


def test_TabETLHDP_LoadCalendar_hashable():
    now = datetime.datetime.now()
    s1 = TabETLHDP_LoadCalendar(f_id=1, dttm=now, project="project1", status="some-status")
    s2 = TabETLHDP_LoadCalendar(f_id=1, dttm=now, project="project1", status="some-status")
    s3 = TabETLHDP_LoadCalendar(f_id=1, dttm=now, project="project1", status="new-status")

    assert hash(s1) == hash(("project1", 1, "some-status", now))
    assert s1 == s2
    assert len(set([s1])) == 1
    assert len(set([s1, s2])) == 1
    assert len(set([s1, s2, s3])) == 2
