from unittest import TestCase
import os
from fu import sqlite_kv as kv


class TestSqliteKv(TestCase):
    def setUp(self) -> None:
        self.filepath = "kv.db"
        self.db = kv.SqliteCache(self.filepath)

    def tearDown(self) -> None:
        self.db.conn.close()
        os.remove(self.filepath)

    def testAll(self):
        self.db.put("one", 1)
        print(self.db.query("one"))
        self.db.put("one", "two")
        print(self.db.query("one"))
        self.db.remove("one")
        print(self.db.query("one"))
