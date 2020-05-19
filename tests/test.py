from fu import sqlite_util as db
# conn=db.get_conn("haha.db")
# db.init_structure(conn,"""
# create table haha(name varchar(10))
# """)

class Haha:
    def __init__(self):
        self.name="weiyinfu"
print(type(Haha))
print(dir(Haha))