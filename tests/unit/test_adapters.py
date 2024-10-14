import os
import unittest
import pytest

from unittest.mock import MagicMock

import app.src.adapters as adapters


class TestConnection(unittest.TestCase):

    def setUp(self) -> None:
        self.email = adapters.Email()

    def test_get_environment_type(self):
        self.assertTrue(isinstance(adapters.get_environment_type(), str))

    def test_get_settings(self):
        settings = adapters.get_settings()
        self.assertIsInstance(settings, dict)
        self.assertIn("modb", settings)
        self.assertIn("acrm", settings)
        self.assertIn("email", settings)

    def test_Email(self):
        self.assertIsNotNone(self.email.server)
        self.assertIsNotNone(self.email.port)
        self.assertIsNotNone(self.email.username)
        self.assertIsNotNone(self.email.password)
        self.assertIsNotNone(self.email.sender)

    # def test_get_email_template(self):
    #     file = "template.html"
    #     template = get_email_template(file)
    #     self.assertIsInstance(template, jinja2.Template)

#  switch to pytest here

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

def test_is_listener():
    listener_name = "server-name-LS"
    assert adapters.is_listener(listener_name)

    some_node_name = "server-name-n1"
    assert not adapters.is_listener(some_node_name)


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
    mock_conn.cursor.fetchone.return_value = (active_node_name, )
    mock_engine = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_conn

    assert active_node_name == adapters.get_active_node_name(mock_engine)

def test_get_connection_string():
    param = {
        'username': 'value-1',
        'password': 'value-2',
        'server': 'value-3',
        'database': 'value-5',
    }
    for key in param:
        assert param[key] in adapters.get_connection_string(param)

if __name__ == '__main__':
    
    unittest.main()