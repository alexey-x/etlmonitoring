import abc
import schedule
from sqlalchemy import text

from typing import Iterable, Any

from app.src.notify import notify
from app.src.adapters import (
    get_settings,
    get_session,
    get_connect_db,
    get_sql_query,
    Role,
)

from app.src.model import (
    TabScenario,
    TabMOOffersAgg,
    TabMOSegments,
    TabETLHDP_LoadCalendar,
)

from app.src.stat_objects import calc_stat


class ControlObject(abc.ABC):
    @abc.abstractmethod
    def get_data(self) -> Iterable:
        """Implement data aquisition method for the given control object."""
        ...

    @abc.abstractmethod
    def process_data(self, data: Iterable[Any]) -> None:
        """Implement data handling logic."""
        ...


class SegmentMODB(ControlObject):
    event = "Новые сегменты загружены в MODB"
    database = "modb"
    sql = "co_SegmentMODB.sql"
    model = TabMOSegments
    message_template = "email_co_SegmentMODB.j2"
    run_on_schedule = schedule.every(5).minutes.do  # ref to function

    def __init__(self) -> None:
        self.engine = get_connect_db(self.database, get_settings())
        self.query = get_sql_query(self.sql)

    def get_data(self) -> list[TabMOSegments]:
        with get_session(self.engine) as session:
            return session.query(self.model).from_statement(text(self.query)).all()

    def process_data(self, data: set[TabMOSegments]) -> None:
        message_param = {
            "event": self.event,
            "data": data,
            "stat": calc_stat(stat_obj_keys=[]),
        }
        notify(message_param, self.message_template, Role.USER)


class MOOffersAgg(ControlObject):
    event = "Новые строки в INTEGRATION.MO_OFFERS БД MODB"
    database = "modb"
    sql = "co_MOOffersAgg.sql"
    model = TabMOOffersAgg
    message_template = "email_co_MOOffersAgg.j2"
    run_on_schedule = schedule.every().hour.at(":30").do

    def __init__(self) -> None:
        self.engine = get_connect_db(self.database, get_settings())
        self.query = get_sql_query(self.sql)

    def get_data(self) -> list[TabMOOffersAgg]:
        with get_session(self.engine) as session:
            return session.query(self.model).from_statement(text(self.query)).all()

    def process_data(self, data: set[TabMOOffersAgg]) -> None:
        message_param = {
            "event": self.event,
            "data": data,
            "stat": calc_stat(stat_obj_keys=[]),
        }
        notify(message_param, self.message_template, Role.USER)


class ScenarioMODB(ControlObject):
    event = "Создан новый сценарий оптимизации"
    database = "modb"
    sql = "co_ScenarioMODB.sql"
    model = TabScenario
    message_template = "email_co_ScenarioMODB.j2"
    run_on_schedule = schedule.every(5).minutes.do

    def __init__(self) -> None:
        self.engine = get_connect_db(self.database, get_settings())
        self.query = get_sql_query(self.sql)

    def get_data(self) -> list[TabScenario]:
        with get_session(self.engine) as session:
            return session.query(self.model).from_statement(text(self.query)).all()

    def process_data(self, data: set[TabScenario]) -> None:
        message_param = {
            "event": self.event,
            "data": data,
            "stat": calc_stat(stat_obj_keys=[]),
        }
        notify(message_param, self.message_template, Role.USER)


class ScoreAltScoreLTV(ControlObject):
    event = "Статус загрузки скорров и LTV в STAGE и MODB"
    database = "stage"
    sql = "co_ScoreAltScoreLTV.sql"
    model = TabETLHDP_LoadCalendar
    message_template = "email_co_ScoreAltScoreLTV.j2"
    run_on_schedule = schedule.every(5).minutes.do

    def __init__(self) -> None:
        self.engine = get_connect_db(self.database, get_settings())
        self.query = get_sql_query(self.sql)

    def get_data(self) -> list[TabETLHDP_LoadCalendar]:
        with get_session(self.engine) as session:
            return session.query(self.model).from_statement(text(self.query)).all()

    def process_data(self, data: set[TabETLHDP_LoadCalendar]) -> None:
        """
        stat_obj_keys - list of keys to calculate some statistics.
        The keys must be in the stat_objects.STAT_OBJECTS dictionary or nothing will be calculated.
        """
        stat_obj_keys = [(row.project, row.status) for row in data]
        message_param = {
            "event": self.event,
            "data": data,
            "stat": calc_stat(stat_obj_keys),
        }
        notify(message_param, self.message_template, Role.USER)


class SegmentPilotCommRotation(ControlObject):
    event = "PILOT_COMM_ROTATION"
    database = "stage"
    sql = "co_SegmentPilotCommRotation.sql"
    model = TabETLHDP_LoadCalendar
    message_template = "email_co_SegmentPilotCommRotation.j2"
    run_on_schedule = schedule.every(5).minutes.do

    def __init__(self) -> None:
        self.engine = get_connect_db(self.database, get_settings())
        self.query = get_sql_query(self.sql)

    def get_data(self) -> list[TabETLHDP_LoadCalendar]:
        with get_session(self.engine) as session:
            return session.query(self.model).from_statement(text(self.query)).all()

    def process_data(self, data: set[TabETLHDP_LoadCalendar]) -> None:
        """
        stat_obj_keys - list of keys to calculate some statistics.
        The keys must be in the stat_objects.STAT_OBJECTS dictionary or nothing will be calculated.
        """
        stat_obj_keys = [(row.project, row.status) for row in data]
        message_param = {
            "event": self.event,
            "data": data,
            "stat": calc_stat(stat_obj_keys),
        }
        notify(message_param, self.message_template, Role.USER)


class SegmentToMO(ControlObject):
    event = "SEGMENT_TO_MO"
    database = "stage"
    sql = "co_SegmentToMO.sql"
    model = TabETLHDP_LoadCalendar
    message_template = "email_co_SegmentToMO.j2"
    run_on_schedule = schedule.every(5).minutes.do

    def __init__(self) -> None:
        self.engine = get_connect_db(self.database, get_settings())
        self.query = get_sql_query(self.sql)

    def get_data(self) -> list[TabETLHDP_LoadCalendar]:
        with get_session(self.engine) as session:
            return session.query(self.model).from_statement(text(self.query)).all()

    def process_data(self, data: set[TabETLHDP_LoadCalendar]) -> None:
        message_param = {"event": self.event, "data": data, "stat": calc_stat([])}
        notify(message_param, self.message_template, Role.USER)


class RotationToMO(ControlObject):
    event = "ROTATION_TO_MO"
    database = "stage"
    sql = "co_RotationToMO.sql"
    model = TabETLHDP_LoadCalendar
    message_template = "email_co_RotationToMO.j2"
    run_on_schedule = schedule.every(5).minutes.do

    def __init__(self) -> None:
        self.engine = get_connect_db(self.database, get_settings())
        self.query = get_sql_query(self.sql)

    def get_data(self) -> list[TabETLHDP_LoadCalendar]:
        with get_session(self.engine) as session:
            return session.query(self.model).from_statement(text(self.query)).all()

    def process_data(self, data: set[TabETLHDP_LoadCalendar]) -> None:
        message_param = {"event": self.event, "data": data, "stat": calc_stat([])}
        notify(message_param, self.message_template, Role.USER)


class ResultsMOToMA(ControlObject):
    event = "RESULTS_MO_TO_MA"
    database = "stage"
    sql = "co_ResultsMOToMA.sql"
    model = TabETLHDP_LoadCalendar
    message_template = "email_co_ResultsMOToMA.j2"
    run_on_schedule = schedule.every(5).minutes.do

    def __init__(self) -> None:
        self.engine = get_connect_db(self.database, get_settings())
        self.query = get_sql_query(self.sql)

    def get_data(self) -> list[TabETLHDP_LoadCalendar]:
        with get_session(self.engine) as session:
            return session.query(self.model).from_statement(text(self.query)).all()

    def process_data(self, data: set[TabETLHDP_LoadCalendar]) -> None:
        message_param = {"event": self.event, "data": data, "stat": calc_stat([])}
        notify(message_param, self.message_template, Role.USER)
