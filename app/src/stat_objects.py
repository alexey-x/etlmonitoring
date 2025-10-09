import abc
import re
import traceback
import datetime
import sqlalchemy
import enum
import pandas as pd
from sqlalchemy.types import TypeEngine

from app.src.services import notify_admin
from app.src.adapters import (
    get_settings,
    get_connect_db,
    get_sql_query,
)

CSS_TABLE_ID = "stat_report"
PILOT_COMM_ROTAION_NO_DATA_MSG = "Нет данных по сегменту PILOT_COMM_ROTATION"


#  These statuses must correlate with CSS from email_base.j2 template
class DataStatus(enum.StrEnum):
    SUCSESS = "sucsess"
    FAILURE = "failure"
    ERROR = "error"


def select_alter_score_tables_with_max_date(tables: list[str]) -> list[str]:
    """
    Select list of strings containing 14 digits in row. Example SCORE_MODEL_RESULTS_ALTER_20240826170221_3.
    Select list containnig lexigraphic max from these 14 digits. Example 20240826170221 > 20240725170111.
    """
    max_date = []
    for t in tables:
        if (match := re.search(r"(\d{12,14})_", t)) is None:
            continue
        max_date.append(match.group(0))

    if len(max_date) > 0:
        max_date = max(max_date)
    else:
        return []
    return [t for t in tables if max_date in t]


def select_alter_score_table_names(engine: TypeEngine) -> list[str]:
    """Get the most recent tables from the list SCORE_MODEL_RESULTS_ALTER_YYYYMMDDhhmmss_[1,2,3, ...]"""
    query = sqlalchemy.sql.text("""
    select
        TABLE_SCHEMA + '.' + TABLE_NAME
    from INFORMATION_SCHEMA.TABLES
    where TABLE_NAME like 'SCORE_MODEL_RESULTS_ALTER_2%'
    order by TABLE_NAME desc
    """)
    with engine.connect() as conn:
        cursor = conn.execute(query)
        result = cursor.fetchall()
    return [r[0] for r in result]


class StatData:
    def __init__(
        self,
        name: str,
        data: pd.DataFrame = pd.DataFrame(),
        data_status: str | None = None,
    ) -> None:
        self.data_name = name
        self.data_table = self.convert_to_html_table(data)
        self.data_status = data_status

    def convert_to_html_table(self, df: pd.DataFrame) -> str:
        if df.empty:
            return ""

        # convert int number 1000000 to string  "1 000 000" (prettify)
        for col in df.columns:
            if df[col].dtypes == "int64":
                df[col] = df[col].apply(lambda x: f"{int(x):,d}".replace(",", " "))

        return df.to_html(index=False, table_id=CSS_TABLE_ID, na_rep="")

    def __repr__(self) -> str:
        return f"""
        {self.data_name}
        {self.data_table}
        """


class StatObject(abc.ABC):
    @abc.abstractmethod
    def get_stat(self) -> StatData: ...


class StatScoresMO(StatObject):
    database = "modb"
    sql = "stat_StatScoresMO.sql"
    data_name = "Статистика скорров загруженных в MODB"

    def __init__(self) -> None:
        self.engine = get_connect_db(self.database, get_settings())
        self.query = get_sql_query(self.sql)

    def get_stat(self) -> StatData:
        with self.engine.connect() as conn:
            df = pd.read_sql_query(self.query, conn)

        return StatData(name=self.data_name, data=df)


class StatLTVMO(StatObject):
    database = "modb"
    sql = "stat_StatLTVMO.sql"
    data_name = "Статистика LTV в MODB"

    def __init__(self) -> None:
        self.engine = get_connect_db(self.database, get_settings())
        self.query = get_sql_query(self.sql)

    def get_stat(self) -> StatData:
        with self.engine.connect() as conn:
            df = pd.read_sql_query(self.query, conn)

        return StatData(name=self.data_name, data=df)


class StatScoresAlterMO(StatObject):
    _REPLACE = "$ALTER_SCORES$"
    database = "modb"
    sql = "stat_StatScoresAlterMO.sql"  # IMPORTANT! - the same _REPLACE pattern must be inside sql template
    data_name = (
        f"Статистика альтернативных скорров загруженных в MODB в таблицу {_REPLACE}"
    )

    def __init__(self) -> None:
        self.engine = get_connect_db(self.database, get_settings())
        self.query = get_sql_query(self.sql)

    def get_stat(self) -> list[StatData]:
        """
        Calculate statistics for every score table.
        Calculate statistics for unioned score tables.
        Unioned statistics should go in the first place.
        """
        alter_scores_tables = select_alter_score_table_names(self.engine)
        alter_scores_tables = select_alter_score_tables_with_max_date(
            alter_scores_tables
        )
        if not alter_scores_tables:
            return []

        all_stat = []
        with self.engine.connect() as conn:
            # let the statistics for all score tables goes first
            df = pd.read_sql_query(
                self._make_query_to_all_tables(alter_scores_tables), conn
            )
            all_stat.append(StatData(name=self._get_data_name_total(), data=df))

            # calc statistcs for every score table
            for table in alter_scores_tables:
                df = pd.read_sql_query(self._get_query(table), conn)
                all_stat.append(StatData(name=self._get_data_name(table), data=df))

        return all_stat

    def _get_query(self, table: str) -> str:
        return self.query.replace(self._REPLACE, table)

    def _get_data_name(self, table: str) -> str:
        return self.data_name.replace(self._REPLACE, table)

    def _get_data_name_total(self):
        """Returns table name for the summed (unioned) alter scores"""
        return "Суммарная статистика альтернативных скорров загруженных в MODB"

    def _make_query_to_all_tables(self, all_tables: list[str]) -> str:
        query = [f"select * from {table} " for table in all_tables]
        query = "union all\n".join(query)
        query = "".join([" ( ", query, " ) "])
        return self._get_query(query)


class StatScoresStage(StatObject):
    database = "stage"
    sql = "stat_StatScoresStage.sql"
    data_name = "Статистика скорров загруженных в STAGE"

    def __init__(self) -> None:
        self.engine = get_connect_db(self.database, get_settings())
        self.query = get_sql_query(self.sql)

    def get_stat(self) -> StatData:
        with self.engine.connect() as conn:
            df = pd.read_sql_query(self.query, conn)

        return StatData(name=self.data_name, data=df)


class StatLTVStage(StatObject):
    database = "stage"
    sql = "stat_StatLTVStage.sql"
    data_name = "Статистика LTV загруженных в STAGE"

    def __init__(self) -> None:
        self.engine = get_connect_db(self.database, get_settings())
        self.query = get_sql_query(self.sql)

    def get_stat(self) -> StatData:
        with self.engine.connect() as conn:
            df = pd.read_sql_query(self.query, conn)

        return StatData(name=self.data_name, data=df)


class StatScoresAlterStage(StatObject):
    database = "stage"
    sql = "stat_StatScoresAlterStage.sql"
    data_name = "Статистика альтернативных скорров загруженных в STAGE"

    def __init__(self) -> None:
        self.engine = get_connect_db(self.database, get_settings())
        self.query = get_sql_query(self.sql)

    def get_stat(self) -> StatData:
        with self.engine.connect() as conn:
            df = pd.read_sql_query(self.query, conn)

        return StatData(name=self.data_name, data=df)


class StatPilotCommRotationStage(StatObject):
    database = "stage"
    sql = "stat_StatPilotCommRotationStage.sql"
    data_name = {
        DataStatus.SUCSESS: "Завершилась загрузка сегмента PILOT_COMM_ROTATION из Хадуп в STAGE CRM",
        DataStatus.FAILURE: (
            "Завершилась загрузка сегмента PILOT_COMM_ROTATION из Хадуп в STAGE CRM с разными датами."
            f"Ожидаемая дата {datetime.datetime.today().date()}"
        ),
    }

    def __init__(self) -> None:
        self.engine = get_connect_db(self.database, get_settings())
        self.query = get_sql_query(self.sql)
        self.data_status = None

    def get_stat(self) -> StatData:
        with self.engine.connect() as conn:
            df = pd.read_sql_query(self.query, conn)

        self.set_data_status(df)

        return StatData(
            name=self.data_name[self.data_status],
            data=df,
            data_status=str(self.data_status),
        )

    def set_data_status(self, data: pd.DataFrame) -> None:
        if data.empty:
            self.data_status = DataStatus.FAILURE

        # T_SYS_DATETIME - see query  stat_StatPilotCommRotationStage.sql
        dttm = pd.to_datetime(data.at[0, "T_SYS_DATETIME"])
        if dttm.date() == datetime.datetime.today().date():
            self.data_status = DataStatus.SUCSESS
        else:
            self.data_status = DataStatus.FAILURE


class StatPilotCommRotationACRM(StatObject):
    database = "stage"
    sql = "stat_StatPilotCommRotationACRM.sql"
    data_name = {
        DataStatus.SUCSESS: "Завершилась загрузка сегмента PILOT_COMM_ROTATION из STAGE CRM (P4MS) в МА (P1MS)",
        DataStatus.FAILURE: (
            "Завершилась загрузка сегмента PILOT_COMM_ROTATION из STAGE CRM (P4MS) в МА (P1MS) c разными датами."
            f"Ожидаемая дата {datetime.datetime.today().date()}"
        ),
    }

    def __init__(self) -> None:
        self.engine = get_connect_db(self.database, get_settings())
        self.query = get_sql_query(self.sql)
        self.data_status = None

    def get_stat(self) -> StatData:
        with self.engine.connect() as conn:
            df = pd.read_sql_query(self.query, conn)

        self.set_data_status(df)

        return StatData(
            name=self.data_name[self.data_status],
            data=df,
            data_status=str(self.data_status),
        )

    def set_data_status(self, data: pd.DataFrame) -> None:
        if data.empty:
            self.data_status = DataStatus.FAILURE

        # DTTM - see query  stat_StatPilotCommRotationACRM.sql
        dttm = pd.to_datetime(data.at[0, "DTTM"])
        if dttm.date() == datetime.datetime.today().date():
            self.data_status = DataStatus.SUCSESS
        else:
            self.data_status = DataStatus.FAILURE


# See table ETL_HDP.LOAD_CALENDAR columns PROJECT and STATUS
# For each of the projects ('MO_MONTHLY_ALTER',  'MO_LTV', 'MO_MONTHLY')
# calculate statistics when STATUS in (SAS_COMPLETE, STAGE_COMPLETE)
STAT_OBJECTS = {
    ("MO_MONTHLY", "SAS_COMPLETE"): StatScoresMO(),
    ("MO_LTV", "SAS_COMPLETE"): StatLTVMO(),
    ("MO_MONTHLY_ALTER", "SAS_COMPLETE"): StatScoresAlterMO(),
    ("MO_MONTHLY", "STAGE_COMPLETE"): StatScoresStage(),
    ("MO_LTV", "STAGE_COMPLETE"): StatLTVStage(),
    ("MO_MONTHLY_ALTER", "STAGE_COMPLETE"): StatScoresAlterStage(),
    ("CMDM_BRT", "STAGE_COMPLETE"): StatPilotCommRotationStage(),
    ("CMDM_BRT", "SAS_COMPLETE"): StatPilotCommRotationACRM(),
    # ("add", "here"): OtherObjects() from other tables and databases
}


def calc_stat(stat_obj_keys: list[tuple[str, str]]) -> list[StatData]:
    """Calculate statistics for the given table."""
    if not stat_obj_keys:
        return None
    stat = []
    for key in stat_obj_keys:
        _obj = STAT_OBJECTS.get(key)
        if _obj is None:
            continue
        try:
            _obj_stat = _obj.get_stat()
            if isinstance(_obj_stat, list):
                stat.extend(_obj_stat)
            stat.append(_obj_stat)
        except Exception:
            notify_admin(
                event=f"CALC STAT DATA ERROR {key}", data=traceback.format_exc()
            )
            stat.append(StatData(name=f"{_obj.data_name} не рассчитана"))

    return stat
