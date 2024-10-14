import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


from unittest.mock import patch
from typing import Iterable, List

from app.src.collectors import (
    Collector,
)
from app.src.model import (
    TabMAProcessLoadStatus,
    Base,
)
from app.src.adapters import (
    logger,
)


def test_collect():
    class ControlObject:
        pass
    class Logger:
        pass
    with patch.object(Collector, "collect", return_value=None, autospec=True) as mock_collect:
        collector = Collector(ControlObject, Logger())
    mock_collect.assert_called_once()


@pytest.fixture()
def db_session() -> Session:
    engine = create_engine("sqlite:///:memory:", echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(bind=engine)
    yield session
    session.close()

@pytest.fixture()
def fake_object(db_session):
    class FakeControlObject:
        model = TabMAProcessLoadStatus

        def __init__(self) -> None:
            self.session = db_session
            #self.query = 

        def get_data(self) -> List[TabMAProcessLoadStatus]:
            return self.session.query(self.model).all()

        def notify(self, data: Iterable) -> None:
            pass
    return FakeControlObject


def test_TabMAProcessLoadStatus_dbwork(fake_object, db_session):
    
    co = Collector(fake_object, logger)

    assert len(co.tracing_data) == 0

    row = TabMAProcessLoadStatus(process_name="offers_transfer", load_id=1, status="new")
    db_session.add(row)
    db_session.commit()
    print("\n----")
    print(db_session.query(TabMAProcessLoadStatus).all())
    
    co.tracing_data = co.collect()
    print(co.tracing_data)

    assert len(co.tracing_data) == 1
    # update
    row.status = "success"
    db_session.commit()
    print(db_session.query(TabMAProcessLoadStatus).all())