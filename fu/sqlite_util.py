import sqlite3
import re
from typing import List, Tuple
"""
sqlite的常用方法
"""

def get_conn(db_path: str):
    return sqlite3.connect(db_path, check_same_thread=False)


def exist_table(conn: sqlite3.Connection, table_name: str):
    res = conn.execute(f"SELECT * FROM sqlite_master WHERE tbl_name='{table_name}'")
    return res.fetchone() is not None


def init_structure(conn: sqlite3.Connection, sql: str):
    g = re.search("^create\\s+table\\s+(\\w+)", sql, re.IGNORECASE | re.MULTILINE)
    table_name = g[1]
    conn.execute(f"DROP TABLE  IF EXISTS  {table_name} ")
    conn.execute(sql)
    conn.commit()


def to_json(cursor: sqlite3.Cursor, row: List[Tuple]):
    # 将一行数据和cursor转化为一个dict
    a = {}
    for col, row_value in zip(cursor.description, row):
        a[col[0]] = row_value
    return a
