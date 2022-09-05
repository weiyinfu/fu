import re
import sqlite3
from typing import List, Tuple, Iterable, Union, Any, Dict

from fu import dict_obj

"""
sqlite的常用方法
"""


def get_conn(db_path: str):
    return sqlite3.connect(db_path, check_same_thread=False, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)


def exist_table(conn: sqlite3.Connection, table_name: str):
    """
    判断数据库表是否存在

    :param conn: 数据库连接
    :param table_name: 表名
    :return: bool值，表示数据库是否存在
    """
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


def select_list(conn: sqlite3.Connection, sql: str, args: Iterable = tuple()):
    assert isinstance(args, Iterable)
    cursor = conn.execute(sql, args)
    return [to_json(cursor, i, obj_type=dict_obj.DictObj) for i in cursor.fetchall()]


def select_one(conn: sqlite3.Connection, sql: str, args: Iterable = tuple()):
    """
    从数据库中选择一条数据，如果实际数据不是一条，会报错

    :param conn:
    :param sql:
    :param args:
    :return:
    """
    li = select_list(conn, sql, args)
    if len(li) != 1:
        raise Exception(f"{sql} return result length error :len={len(li)}")
    return li[0]


def select_value(conn: sqlite3.Connection, sql: str, args: Iterable = tuple()):
    """
    选择的返回值只有一列，例如select count(1) from ..

    :param args:
    :param conn:
    :param sql:
    :return:
    """
    cursor = conn.execute(sql, args)
    obj = cursor.fetchone()
    if len(obj) != 1:
        raise Exception(f"multi column found {obj}")
    return obj[0]


def insert_one(conn: sqlite3.Connection, table: str, obj: Union[object, Dict[str, Any]], fields: List[str]) -> int:
    """
    向数据库中插入一条数据

    :param obj:
    :param table:
    :param fields:
    :param conn:
    :return: row_count
    """
    field_list = ','.join(fields)
    quote_list = ','.join('?' * len(fields))
    get = getattr
    if type(obj) == dict:
        get = lambda x, k: x[k]
    values = [get(obj, i) for i in fields]
    res = conn.execute(f"insert into {table} ({field_list}) values ({quote_list})", values)
    conn.commit()
    return res.rowcount


def update(conn: sqlite3.Connection, table: str, obj: Union[object, Dict[str, Any]], update_fields: List[str], filter_fields: List[str]):
    if len(filter_fields) == 0:
        raise Exception(f"filter fields = 0 ")
    if len(update_fields) == 0:
        raise Exception(f"update fields = 0")
    set_list = [f'{k}=?' for k in update_fields]
    set_str = ','.join(set_list)
    where_list = [f"{k}=?" for k in filter_fields]
    where_str = ' and '.join(where_list)
    get = getattr
    if type(obj) == dict:
        get = lambda x, k: x[k]
    values = [get(obj, i) for i in update_fields + filter_fields]
    sql = f"update {table} set {set_str} where {where_str}"
    res = conn.execute(sql, values)
    conn.commit()
    return res.rowcount


def insert_many(conn: sqlite3.Connection, table: str,
                obj_list: List[Union[object, Dict[str, Any]]],
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

    def get(obj, i):
        if type(obj_list[0]) == dict:
            return obj[i]
        return getattr(obj, i)

    batch_data = [[get(obj, i) for i in fields] for obj in obj_list]
    res = conn.executemany(sql, batch_data)
    conn.commit()
    return res.rowcount


class Database:
    """
    Database是对上面函数的直接封装，它是另一种用法
    """

    def __init__(self, dbfile: str):
        self.conn = get_conn(dbfile)

    def select_obj(self, sql: str, args: Iterable = tuple()):
        return select_list(self.conn, sql, args)

    def exist_table(self, table_name: str):
        return exist_table(self.conn, table_name)

    def init_structure(self, sql: str):
        return init_structure(self.conn, sql)

    def insert_one(self, table: str, obj: dict_obj.DictObj, fields: List[str]):
        return insert_one(self.conn, table, obj, fields)

    def insert_batch(self, table: str, obj_list: List[dict_obj.DictObj], fields: List[str]) -> int:
        return insert_many(self.conn, table, obj_list, fields)


if __name__ == '__main__':
    update(None, "one", {'x': 1, 'y': 2}, ['x'], ['y'])
