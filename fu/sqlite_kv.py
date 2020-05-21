"""
基于sqlite实现的简易redis
"""

from fu import sqlite_util as d


class SqliteCache:
    """
    使用sqlite模拟一个KV存储，主要是为了提高网站响应速度，同时减少内存占用
    """

    def __init__(self, filepath: str):
        self.conn = d.get_conn(filepath)
        d.init_structure(self.conn, "CREATE TABLE  kv (key VARCHAR(128) PRIMARY KEY ,value longtext)")

    def query(self, k, type_=str):
        res = self.conn.execute("SELECT value FROM kv WHERE key =?", (k,)).fetchone()
        if not res:
            return None
        else:
            return type_(res[0])

    def remove(self, k):
        self.conn.execute("DELETE FROM kv WHERE key=?", (k,))
        self.conn.commit()

    def put(self, k, v):
        old_value = self.query(k)
        if not old_value:
            sql = "INSERT INTO kv VALUES (?,?)"
            self.conn.execute(sql, (k, v))
        else:
            sql = "UPDATE kv SET VALUE =? WHERE key=?"
            self.conn.execute(sql, (v, k))
        self.conn.commit()
