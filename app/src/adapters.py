import os
import sys
import socket
import json
import jinja2
import logging
import logging.config

sys.path.append(os.path.abspath(".."))
sys.path.append(os.path.abspath("."))


from enum import Enum
from typing import Dict, List
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.types import TypeEngine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager

from app.src import encryption


ROOTPATH = Path("/mo/monitor_etl")
CONFIGPATH = ROOTPATH / "config"
LOG_CONFIG = CONFIGPATH / "logging.conf"
TEMPLATES = ROOTPATH / "templates"
SQL_QUERIES = ROOTPATH / "sql"


logging.config.fileConfig(LOG_CONFIG)
logger = logging.getLogger()


class Role(Enum):
    """
    Roles to filter notifications. ADMIN gets all notifications.
    Roles are set in the recipients.json file.
    """

    ADMIN = "admin"
    USER = "user"


def is_listener(server: str) -> bool:
    """If server is a listener its name ends on LS, e.g. S-RTO-P3MS-LS."""
    return server.upper().endswith("LS")


def get_passive_node_name(server: str) -> str:
    """If the active node has the name like S-RTO-P3MS-N1.
    The passive node has the name like S-RTO-P3MS-N2 and vice versa."""
    if server[-1] == "1":
        return f"{server[:-1]}2"
    elif server[-1] == "2":
        return f"{server[:-1]}1"
    else:
        raise ValueError(f"Failed to get passive node from {server}")


def get_active_node_name(engine: TypeEngine) -> str:
    """The query "select @@SERVERNAME" points to active node."""
    with engine.connect() as conn:
        cursor = conn.execute("select @@SERVERNAME")
        result = cursor.fetchone()
    if result:
        return result[0]
    raise ValueError(f"Failed to fetch active node name using engine {engine}")


def get_connection_string(param: Dict) -> str:
    port = 1433
    return f"mssql+pymssql://{param['username']}:{param['password']}@{param['server']}:{port}/{param['database']}"


def get_connect_db(dbname: str, settings: Dict) -> TypeEngine:
    param = settings[dbname]
    param["password"] = encryption.decrypt(param["password"])

    if not (is_listener(param["server"]) and settings["use_passive_node"]):
        return create_engine(get_connection_string(param), echo=False)

    param["server"] = get_passive_node_name(get_active_node_name(param["server"]))

    return create_engine(get_connection_string(param), echo=False)


def get_environment_type() -> str:
    """Decide what settings to use [prod, test, ]."""
    host = socket.gethostname()
    with (CONFIGPATH / "host.json").open(encoding="UTF-8") as f:
        host_map = json.load(f)
    return host_map[host]


def get_settings() -> Dict:
    settings_file = CONFIGPATH / get_environment_type() / "settings.json"
    with settings_file.open(encoding="UTF-8") as f:
        return json.load(f)


@contextmanager
def get_session(engine) -> Session:
    Session = sessionmaker(bind=engine, expire_on_commit=False)
    session = Session()
    try:
        yield session
    except Exception:
        session.rollback()
    finally:
        session.close()


def get_recipients(role: Role) -> List[str]:
    settings_file = CONFIGPATH / get_environment_type() / "recipients.json"
    with settings_file.open(encoding="UTF-8") as f:
        return [
            recipient
            for recipient, param in json.load(f).items()
            if param["active"] and param["role"] in [role.value, Role.ADMIN.value]
        ]


# make it dataclass when switch to python3.12
class Email:
    def __init__(self) -> None:
        settings = get_settings()["email"]
        self.server = settings["server"]
        self.port = int(settings["port"])
        self.username = settings["username"]
        self.password = encryption.decrypt(settings["password"])
        self.sender = f"{self.username}@{settings['domen']}"


def get_email_template(template_file_name: str) -> jinja2.Template:
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATES))
    return env.get_template(template_file_name)


def get_sql_query(query: str) -> str:
    return (SQL_QUERIES / query).read_text()
