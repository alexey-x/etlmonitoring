from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Date

Base = declarative_base()


class TabMAProcessLoadStatus(Base):
    """It seems with the switch to Airflow this class is not needed anymore. TOBE removed!!!"""

    __tablename__ = "MA_PROCESS_LOAD_STATUS"  # acrmsas.CDM.MA_PROCESS_LOAD_STATUS
    # __table_args__ = {"schema": "CDM"}

    process_name = Column(String(128))
    log_dttm = Column(DateTime)
    finish_dttm = Column(DateTime)
    update_dttm = Column(DateTime)
    apc_campaign_name = Column(String(128))
    file_name = Column(String(128))
    status = Column(String(128), primary_key=True)
    user_name = Column(String(128))
    error_text = Column(String(400))
    load_id = Column(Integer, primary_key=True)
    file_operation = Column(String(400))
    message = Column(String(4000))

    def __repr__(self) -> str:
        return f"""
        MAProcessLoadStatus[
            process_name = {self.process_name!r}, 
            log_dttm = {self.log_dttm!r}, 
            status = {self.status!r}, 
            load_id = {self.load_id!r}
        ]
        """

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, type(self))
            and self.process_name == other.process_name
            and self.load_id == other.load_id
            and self.status == other.status
        )

    def __hash__(self) -> int:
        return hash((self.process_name, self.load_id, self.status))


class TabScenario(Base):
    __tablename__ = "SCENARIO"  # modb.MO_DATA.SCENARIO
    # __table_args__ = {"schema": "MO_DATA"}

    scenario_id = Column(Integer, primary_key=True)
    scenario_nm = Column(String(128))
    scenario_desc = Column(String(256))
    scenario_period_dd = Column(Integer)
    scenario_period_start_dt_bckp = Column(DateTime)
    scenario_goal = Column(String(128))
    status = Column(String(128))
    status_desc = Column(String(128))
    deleted_flg = Column(Integer)
    created_by = Column(String(256))
    updated_by = Column(String(256))
    last_run_by = Column(String(256))
    last_run_dttm = Column(DateTime)
    last_run_id = Column(Integer)
    created_dttm = Column(DateTime)
    updated_dttm = Column(DateTime)
    edit_dttm = Column(DateTime)
    edit_by = Column(String(256))
    scenario_period_start_dt = Column(Integer)
    delay_days = Column(Integer)
    date_setting_method = Column(String(15))
    start_period_dttm = Column(DateTime)
    end_period_dttm = Column(DateTime)
    is_using_alter_score_ind = Column(Integer)
    size_pct = Column(Integer)
    algo = Column(String(10))
    algo_pct = Column(Integer)
    customer_pct = Column(Integer)
    alter_score_source = Column(String(128))

    def __repr__(self) -> str:
        return f"Scenario(scenario_id = {self.scenario_id!r}, scenario_nm = {self.scenario_nm!r})"

    def __eq__(self, other) -> bool:
        return isinstance(other, type(self)) and self.scenario_id == other.scenario_id

    def __hash__(self) -> int:
        return hash(self.scenario_id)


class TabMOOffersAgg(Base):
    """Agregated MO_OFFERS (see proper query) in sql folder."""

    __tablename__ = "MO_OFFERS"  # modb.INTEGRATION.MO_OFFERS
    # __table_args__ = {"schema": "INTGERATION"}

    segment_cd = Column(String(128), primary_key=True)
    status = Column(String(30), primary_key=True)
    num_offers = Column(Integer)
    created_dttm = Column(DateTime, nullable=False)
    updated_dttm = Column(DateTime, nullable=False)

    def __repr__(self) -> str:
        return f"""
        Offer[
            segment_cd = {self.segment_cd!r}, 
            status = {self.status!r},
            num_offers = {self.num_offers!r},
            created_dttm = {self.created_dttm!r},
            updated_dttm = {self.updated_dttm!r}
        ]
        """

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, type(self))
            and self.segment_cd == other.segment_cd
            and self.status == other.status
            and self.created_dttm == other.created_dttm
            and self.updated_dttm == other.updated_dttm
        )

    def __hash__(self) -> int:
        return hash(
            (self.segment_cd, self.status, self.created_dttm, self.updated_dttm)
        )


class TabMOSegments(Base):
    __tablename__ = "MO_SEGMENTS"  # modb.INTEGRATION.MO_SEGMENTS
    # __table_args__ = {"schema": "INTGERATION"}

    segment_cd = Column(String(128), primary_key=True)
    count = Column(Integer)
    created_dttm = Column(DateTime)

    def __repr__(self) -> str:
        return f"Segment(segment_cd = {self.segment_cd!r})"

    def __eq__(self, other) -> bool:
        return isinstance(other, type(self)) and self.segment_cd == other.segment_cd

    def __hash__(self) -> int:
        return hash(self.segment_cd)


class TabETLHDP_LoadCalendar(Base):
    __tablename__ = "LOAD_CALENDAR"  # acrmsas.ETL_HDP.LOAD_CALENDAR
    # __table_args__ = {"schema": "CDM"}

    f_id = Column(Integer, primary_key=True)
    dt = Column(Date)
    dttm = Column(DateTime)
    project = Column(String(128))
    status = Column(String(300), primary_key=True)
    description = Column(String(1000))
    load_type = Column(Integer)
    cdttm = Column(DateTime)

    def __repr__(self) -> str:
        return f"""
        TabETLHDP_LoadCalendar[
            project = {self.project!r}, 
            dttm = {self.dttm!r}, 
            status = {self.status!r}, 
            f_id = {self.f_id!r}
        ]
        """

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, type(self))
            and self.project == other.project
            and self.f_id == other.f_id
            and self.status == other.status
            and self.dttm == other.dttm
        )

    def __hash__(self) -> int:
        return hash((self.project, self.f_id, self.status, self.dttm))
