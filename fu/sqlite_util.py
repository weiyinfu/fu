import sqlite3
import re
from typing import List, Tuple
from fu import dict_obj

"""
sqlite的常用方法
"""


def get_conn(db_path: str):
    return sqlite3.connect(db_path, check_same_thread=False, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)


def exist_table(conn: sqlite3.Connection, table_name: str):
    res = conn.execute(f"SELECT * FROM sqlite_master WHERE tbl_name='{table_name}'")
    return res.fetchone() is not None


def init_structure(conn: sqlite3.Connection, sql: str):
    g = re.search("^\\s*create\\s+table\\s+(\\w+)", sql, re.IGNORECASE | re.MULTILINE)
    table_name = g[1]
    conn.execute(f"DROP TABLE  IF EXISTS  {table_name} ")
    conn.execute(sql)
    conn.commit()


def to_json(cursor: sqlite3.Cursor, row: List[Tuple], obj_type: type = dict):
    # 将一行数据和cursor转化为一个dict
    a = obj_type()
    for col, row_value in zip(cursor.description, row):
        a[col[0]] = row_value
    return a


def select_json(conn: sqlite3.Connection, sql: str):
    cursor = conn.execute(sql)
    return [to_json(cursor, i) for i in cursor.fetchall()]


def select_obj(conn: sqlite3.Connection, sql: str):
    cursor = conn.execute(sql)
    return [to_json(cursor, i, obj_type=dict_obj.DictObj) for i in cursor.fetchall()]


def select_one_value(conn: sqlite3.Connection, sql: str):
    """
    选择的返回值只有一列，例如select count(1) from ..
    :param conn:
    :param sql:
    :return:
    """
    cursor = conn.execute(sql)
    obj = cursor.fetchone()
    if len(obj) != 1:
        raise Exception(f"multi column found {obj}")
    return cursor.fetchone()[0]


def insert_one(conn: sqlite3.Connection, table: str, obj: dict_obj.DictObj, fields: List[str]) -> int:
    """
    向数据库中插入一条数据
    :param obj:
    :param table:
    :param fields:
    :param conn:
    :return:row_count
    """
    field_list = ','.join(fields)
    quote_list = ','.join('?' * len(fields))
    values = [getattr(obj, i) for i in fields]
    res = conn.execute(f"insert into {table} ({field_list}) values ({quote_list})", values)
    conn.commit()
    return res.rowcount


def insert_many(conn: sqlite3.Connection, table: str,
                obj_list: List[dict_obj.DictObj],
                fields: List[str] = None):
    """
    批量插入数据
    :param obj_list:
    :param conn:
    :param table:
    :param fields:
    :return:
    """
    field_list = ','.join(fields)
    quote_list = ','.join('?' * len(fields))
    sql = f"insert into {table} ({field_list}) values ({quote_list})"
    batch_data = [[getattr(obj, i) for i in fields] for obj in obj_list]
    res = conn.executemany(sql, batch_data)
    conn.commit()
    return res.rowcount


class Database:
    """
    Database是对上面函数的直接封装，它是另一种用法
    """

    def __init__(self, dbfile: str):
        self.conn = get_conn(dbfile)

    def select_json(self, sql: str):
        return select_json(self.conn, sql)

    def select_obj(self, sql: str):
        return select_obj(self.conn, sql)

    def exist_table(self, table_name: str):
        return exist_table(self.conn, table_name)

    def init_structure(self, sql: str):
        return init_structure(self.conn, sql)

    def insert_one(self, table: str, obj: dict_obj.DictObj, fields: List[str]):
        return insert_one(self.conn, table, obj, fields)

    def insert_batch(self, table: str, obj_list: List[dict_obj.DictObj], fields: List[str]) -> int:
        return insert_many(self.conn, table, obj_list, fields)
