import os
import jinja2
import unittest
import pytest
import json

from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path

import app.src.adapters as adapters


# Mock settings data
mock_settings = {
    "email": {
        "server": "smtp.example.com",
        "port": "587",
        "username": "user",
        "password": "encrypted_password",
        "domen": "example.com",
    }
}


# Mock decryption function
def mock_decrypt(password):
    return "decrypted_password"


@pytest.fixture
def mock_get_settings():
    with patch("app.src.adapters.get_settings", return_value=mock_settings):
        yield


@pytest.fixture
def mock_encryption_decrypt():
    with patch("app.src.encryption.decrypt", side_effect=mock_decrypt):
        yield


@pytest.mark.parametrize(
    "settings, expected_server, expected_port, expected_username, expected_password, expected_sender",
    [
        (
            mock_settings,
            "smtp.example.com",
            587,
            "user",
            "decrypted_password",
            "user@example.com",
        ),
    ],
    ids=["happy_path"],
)
def test_email_initialization_happy_path(
    mock_get_settings,
    mock_encryption_decrypt,
    settings,
    expected_server,
    expected_port,
    expected_username,
    expected_password,
    expected_sender,
):
    # Act
    email = adapters.Email()

    # Assert
    assert email.server == expected_server
    assert email.port == expected_port
    assert email.username == expected_username
    assert email.password == expected_password
    assert email.sender == expected_sender


@pytest.mark.parametrize(
    "settings, expected_exception",
    [
        (
            {
                "email": {
                    "server": "smtp.example.com",
                    "port": "not_an_int",
                    "username": "user",
                    "password": "encrypted_password",
                    "domen": "example.com",
                }
            },
            ValueError,
        ),
    ],
    ids=["invalid_port"],
)
def test_email_initialization_edge_cases(
    mock_encryption_decrypt, settings, expected_exception
):
    # Arrange
    with patch("app.src.adapters.get_settings", return_value=settings):
        # Act & Assert
        with pytest.raises(expected_exception):
            adapters.Email()


@pytest.mark.parametrize(
    "settings, expected_exception",
    [
        (
            {
                "email": {
                    "server": "smtp.example.com",
                    "port": "587",
                    "username": "user",
                    "password": "encrypted_password",
                }
            },
            KeyError,
        ),
    ],
    ids=["missing_domen"],
)
def test_email_initialization_error_cases(
    mock_encryption_decrypt, settings, expected_exception
):
    # Arrange
    with patch("app.src.adapters.get_settings", return_value=settings):
        # Act & Assert
        with pytest.raises(expected_exception):
            adapters.Email()


# Mock configuration path
CONFIGPATH = Path("mock/config/path")

# Test data
host_map_data = {"host1": "prod", "host2": "test", "host3": "dev"}


@pytest.mark.parametrize(
    "hostname, expected_env, test_id",
    [
        ("host1", "prod", "happy_path_prod"),
        ("host2", "test", "happy_path_test"),
        ("host3", "dev", "happy_path_dev"),
        ("unknown_host", None, "edge_case_unknown_host"),
    ],
    ids=lambda x: x[2],
)
def test_get_environment_type(hostname, expected_env, test_id):
    # Arrange
    mock_host_map = json.dumps(host_map_data)
    with patch("socket.gethostname", return_value=hostname), patch(
        "builtins.open", mock_open(read_data=mock_host_map)
    ), patch("adapters.CONFIGPATH", CONFIGPATH):
        # Act
        if hostname in host_map_data:
            result = adapters.get_environment_type()

            # Assert
            assert result == expected_env
        else:
            with pytest.raises(KeyError):
                adapters.get_environment_type()


@pytest.mark.parametrize(
    "file_content, expected_exception, test_id",
    [
        ("{invalid_json}", json.JSONDecodeError, "error_case_invalid_json"),
        ("{}", KeyError, "error_case_empty_json"),
    ],
    ids=lambda x: x[2],
)
def test_get_environment_type_errors(file_content, expected_exception, test_id):
    # Arrange
    with patch("socket.gethostname", return_value="host1"), patch(
        "builtins.open", mock_open(read_data=file_content)
    ), patch("adapters.CONFIGPATH", CONFIGPATH):
        # Act & Assert
        with pytest.raises(expected_exception):
            adapters.get_environment_type()


import pytest
import json
from unittest.mock import patch, mock_open
from pathlib import Path
from adapters import get_settings

# Mock configuration
CONFIGPATH = Path("/mock/config/path")


# Helper function to mock get_environment_type
def mock_get_environment_type():
    return "test_env"


@pytest.mark.parametrize(
    "mock_file_content, expected_result, exception, test_id",
    [
        ('{"key": "value"}', {"key": "value"}, None, "happy_path_valid_json"),
        ("{}", {}, None, "happy_path_empty_json"),
        (
            '{"key": "value", "number": 123}',
            {"key": "value", "number": 123},
            None,
            "happy_path_multiple_keys",
        ),
        ("", None, json.JSONDecodeError, "error_empty_file"),
        ("{invalid_json}", None, json.JSONDecodeError, "error_invalid_json"),
    ],
    ids=lambda x: x[-1],
)
def test_get_settings(mock_file_content, expected_result, exception, test_id):
    # Arrange
    mock_path = CONFIGPATH / mock_get_environment_type() / "settings.json"
    with patch("adapters.get_environment_type", side_effect=mock_get_environment_type):
        with patch(
            "pathlib.Path.open", mock_open(read_data=mock_file_content)
        ) as mock_file:
            # Act
            if exception:
                with pytest.raises(exception):
                    result = get_settings()
            else:
                result = get_settings()

            # Assert
            if not exception:
                assert result == expected_result
            mock_file.assert_called_once_with(encoding="UTF-8")


def test_get_sql_query():
    query = "select 1"
    file = "file.sql"
    (adapters.SQL_QUERIES / file).write_text(query)
    assert adapters.get_sql_query(file) == query
    os.unlink(adapters.SQL_QUERIES / file)


def test_get_recipients_admin():
    role = adapters.Role.ADMIN
    recipients = adapters.get_recipients(role)
    developer = "aleksey.voevodkin@gazprombank.ru"
    assert isinstance(recipients, list)
    assert developer in recipients


def test_get_recipients_user():
    role = adapters.Role.USER
    recipients = adapters.get_recipients(role)
    developer = "aleksey.voevodkin@gazprombank.ru"
    assert isinstance(recipients, list)
    assert developer in recipients


def test_get_passive_node_name():
    active_node = "server-n1"
    passive_node = "server-n2"
    assert adapters.get_passive_node_name(active_node) == passive_node

    active_node = "server-n2"
    passive_node = "server-n1"
    assert adapters.get_passive_node_name(active_node) == passive_node

    server_name = "no-nodes"
    with pytest.raises(ValueError):
        adapters.get_passive_node_name(server_name)


def test_get_active_node_name():
    active_node_name = "active-node"
    mock_conn = MagicMock()
    mock_conn.execute.return_value = mock_conn.cursor
    mock_conn.cursor.fetchone.return_value = (active_node_name,)
    mock_engine = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_conn

    assert active_node_name == adapters.get_active_node_name(mock_engine)


def test_get_connection_string():
    param = {
        "username": "value-1",
        "password": "value-2",
        "server": "value-3",
        "database": "value-5",
    }
    for key in param:
        assert param[key] in adapters.get_connection_string(param)


@pytest.mark.parametrize(
    "server, expected, test_id",
    [
        ("S-RTO-P3MS-LS", True, "happy_path_uppercase"),
        ("s-rto-p3ms-ls", True, "happy_path_lowercase"),
        ("S-RTO-P3MS-ls", True, "happy_path_mixed_case"),
        ("S-RTO-P3MS", False, "no_ls_suffix"),
        ("S-RTO-P3MS-L", False, "single_l_suffix"),
        ("", False, "empty_string"),
        ("LS", True, "only_ls"),
        ("LSS", False, "ls_followed_by_s"),
        ("S-RTO-P3MS-LS ", False, "ls_with_trailing_space"),
        (" S-RTO-P3MS-LS", False, "ls_with_leading_space"),
    ],
    ids=lambda x: x[2],
)
def test_is_listener(server, expected, test_id):
    # Act
    result = adapters.is_listener(server)

    # Assert
    assert result == expected


@pytest.mark.parametrize(
    "server, expected, test_id",
    [
        ("S-RTO-P3MS-N1", "S-RTO-P3MS-N2", "happy_path_1_to_2"),
        ("S-RTO-P3MS-N2", "S-RTO-P3MS-N1", "happy_path_2_to_1"),
        ("A-B-C-D1", "A-B-C-D2", "edge_case_simple_1_to_2"),
        ("A-B-C-D2", "A-B-C-D1", "edge_case_simple_2_to_1"),
    ],
    ids=lambda x: x[2],
)
def test_get_passive_node_name_happy_and_edge_cases(server, expected, test_id):
    # Act
    result = adapters.get_passive_node_name(server)

    # Assert
    assert result == expected


@pytest.mark.parametrize(
    "server, expected_exception, test_id",
    [
        ("S-RTO-P3MS-N3", ValueError, "error_case_invalid_suffix_3"),
        ("S-RTO-P3MS-N0", ValueError, "error_case_invalid_suffix_0"),
        ("S-RTO-P3MS-N", ValueError, "error_case_missing_suffix"),
        ("S-RTO-P3MS-NX", ValueError, "error_case_non_numeric_suffix"),
    ],
    ids=lambda x: x[2],
)
def test_get_passive_node_name_error_cases(server, expected_exception, test_id):
    # Act & Assert
    with pytest.raises(expected_exception):
        adapters.get_passive_node_name(server)


# Define a constant for the template directory
TEMPLATES = "path/to/templates"


@pytest.mark.parametrize(
    "template_file_name, expected_template_name",
    [
        ("valid_template.html", "valid_template.html"),  # happy path
        ("another_template.txt", "another_template.txt"),  # happy path
    ],
    ids=[
        "valid_html_template",
        "valid_txt_template",
    ],
)
def test_get_email_template_happy_path(template_file_name, expected_template_name):
    # Arrange
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATES))
    env.get_template = lambda name: jinja2.Template(name)

    # Act
    template = adapters.get_email_template(template_file_name)

    # Assert
    assert template.name == expected_template_name


@pytest.mark.parametrize(
    "template_file_name",
    [
        "",  # edge case: empty string
        "non_existent_template.html",  # error case: non-existent file
    ],
    ids=[
        "empty_template_name",
        "non_existent_template",
    ],
)
def test_get_email_template_edge_and_error_cases(template_file_name):
    # Arrange
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATES))
    env.get_template = lambda name: jinja2.Template(name)

    # Act & Assert
    if template_file_name == "":
        with pytest.raises(jinja2.exceptions.TemplateNotFound):
            adapters.get_email_template(template_file_name)
    else:
        with pytest.raises(jinja2.exceptions.TemplateNotFound):
            adapters.get_email_template(template_file_name)


import pytest
from pathlib import Path
from unittest.mock import patch, mock_open

# Mock SQL_QUERIES path
SQL_QUERIES = Path("/mock/sql/queries")


# Parametrized test for happy path, edge cases, and error cases
@pytest.mark.parametrize(
    "query, file_content, expected, exception, test_id",
    [
        (
            "valid_query.sql",
            "SELECT * FROM table;",
            "SELECT * FROM table;",
            None,
            "happy_path_valid_query",
        ),
        ("empty_query.sql", "", "", None, "edge_case_empty_file"),
        (
            "non_existent.sql",
            None,
            None,
            FileNotFoundError,
            "error_case_non_existent_file",
        ),
        ("invalid_path.sql", None, None, OSError, "error_case_invalid_path"),
    ],
    ids=lambda x: x[-1],
)
def test_get_sql_query(query, file_content, expected, exception, test_id):
    # Mock the file reading behavior
    m_open = (
        mock_open(read_data=file_content) if file_content is not None else mock_open()
    )
    with patch("pathlib.Path.read_text", m_open):
        with patch("pathlib.Path.__truediv__", return_value=SQL_QUERIES / query):
            if exception:
                # Act and Assert
                with pytest.raises(exception):
                    adapters.get_sql_query(query)
            else:
                # Act
                result = adapters.get_sql_query(query)

                # Assert
                assert result == expected


if __name__ == "__main__":
    unittest.main()
