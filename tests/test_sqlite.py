from unittest import TestCase
from fu import sqlite_util as d
import os
from typing import List
from fu.dict_obj import DictObj


class Haha:
    def __init__(self):
        self.haha = ''


class TestSqlite(TestCase):
    def setUp(self) -> None:
        self.filepath = "haha.db"
        self.conn = d.get_conn(self.filepath)
        d.init_structure(self.conn, """
        create table haha(haha int)
        """)
        self.conn.execute("insert into haha values(1),(2),(3)")

    def tearDown(self) -> None:
        print("tearing down")
        self.conn.close()
        os.remove(self.filepath)

    def test_get_json(self):
        print(d.select_json(self.conn, "select * from haha"))

    def test_get_obj(self):
        a: List[Haha] = d.select_obj(self.conn, "select * from haha")
        print(a[0].haha)

    def test_select_one(self):
        res = d.select_one_value(self.conn, "select count(1) from haha")
        print(res)

    def test_insert_one_false(self):
        haha = DictObj({'haha': 'haha'})
        d.insert_one(self.conn, 'haha', haha, ['haha'])
        a = d.select_json(self.conn, 'select * from haha')
        print(a)

    def test_insert_one(self):
        haha = DictObj({'haha': 1})
        res = d.insert_one(self.conn, "haha", haha, ['haha'])
        print(res)

    def test_insert_many(self):
        haha = DictObj({'haha': 1})
        res = d.insert_many(self.conn, "haha", [haha, haha], ['haha'])
        print(res)
