# -*- coding: utf-8 -*-

import sqlite3
from contextlib import closing
import numpy as np
import io

dbname = 'data/database.db'

def adapt_array(arr):
    """
    http://stackoverflow.com/a/31312102/190597 (SoulNibbler)
    """
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())

def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)

# Converts np.array to TEXT when inserting
sqlite3.register_adapter(np.ndarray, adapt_array)

# Converts TEXT to np.array when selecting
sqlite3.register_converter("array", convert_array)

x = np.arange(12).reshape(2,6)

with closing(sqlite3.connect(dbname, detect_types=sqlite3.PARSE_DECLTYPES)) as conn:
    c = conn.cursor()

    
    # executeメソッドでSQL文を実行する
    try:
        drop_table = '''drop table file_index;'''
        c.execute(drop_table)
    except:
        print("---tmp---")

    # executeメソッドでSQL文を実行する
    create_table = '''create table file_index (id int, name varchar(64), arr array)'''
    c.execute(create_table)

    # SQL文に値をセットする場合は，Pythonのformatメソッドなどは使わずに，
    # セットしたい場所に?を記述し，executeメソッドの第2引数に?に当てはめる値を
    # タプルで渡す．
    sql = 'insert into file_index (id, name, arr) values (?,?,?)'
    users = [
        (0, 'dignl-78712', x),
        (1, 'dignl-78713', x)
    ]
    c.executemany(sql, users)
    conn.commit()

    select_sql = 'select * from file_index where name = "' + "dignl-78712" + '"'
    for row in c.execute(select_sql).fetchall():
        print(row)
        print(type(row[2]))
        # print(row[0])