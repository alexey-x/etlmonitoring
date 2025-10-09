import pytest
import datetime

import sys
for _ in sys.path:
    print(_)

from app.src.control_objects import (
    SegmentMODB,
    MOOffersAgg,
    ScenarioMODB,
    ScoreAltScoreLTV,
    SegmentPilotCommRotation,
    SegmentToMO,
    RotationToMO,
    ResultsMOToMA,
)

class FakeTabMOSegments:
    def __init__(self, segment_cd: str, count: int, created_dttm: datetime.datetime) -> None:
        self.segment_cd = segment_cd
        self.count = count
        self.created_dttm = created_dttm

@pytest.fixture()
def provide_FakeTabMOSegments():
    return FakeTabMOSegments


@pytest.fixture(params=[
            SegmentMODB,
            MOOffersAgg,
            ScenarioMODB,
            SegmentPilotCommRotation,
            ScoreAltScoreLTV,
            SegmentToMO,
            RotationToMO,
            ResultsMOToMA,
        ]
    )
def db_control_object(request):
    """Gives clasess of control objects inside databses."""
    return request.param

# @pytest.fixture(scope="session")
# def db() -> Session:
#     engine = create_engine("sqlite:///:memory:", echo=True)
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     Base.metadata.create_all(bind=engine)
#     yield session
#     session.close()