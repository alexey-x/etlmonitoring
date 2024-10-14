import unittest
import sqlalchemy

from app.src.adapters import (
    get_settings,
    get_connect_db,
)

class TestIntegration(unittest.TestCase):

    def setUp(self) -> None:
        self.settings = get_settings()
        self.modb_engine = get_connect_db("modb", self.settings)
        self.acrm_engine = get_connect_db("acrm", self.settings)
        self.stage_engine = get_connect_db("stage", self.settings)

    def test_connect_modb(self):
        query = sqlalchemy.sql.text("select 1")
        with self.modb_engine.connect() as con:
            cursor = con.execute(query)
            result = cursor.fetchall()
        self.assertEqual([(1,)], result)

    def test_connect_acrm(self):
        query = sqlalchemy.sql.text("select 1")
        with self.acrm_engine.connect() as con:
            cursor = con.execute(query)
            result = cursor.fetchall()
        self.assertEqual([(1,)], result)

    def test_connect_stage(self):
        query = sqlalchemy.sql.text("select 1")
        with self.stage_engine.connect() as con:
            cursor = con.execute(query)
            result = cursor.fetchall()
        self.assertEqual([(1,)], result)



if __name__ == '__main__':
    
    unittest.main()