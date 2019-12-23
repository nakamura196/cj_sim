import numpy
import glob
from annoy import AnnoyIndex
from scipy import spatial
import json
import sqlite3
from contextlib import closing
import io

# config
dims = 2048
# n_nearest_neighbors = 1000
trees = 100

t = AnnoyIndex(dims, metric='angular')

image_vectors_path = "../output/image_vectors"
files = glob.glob(image_vectors_path+"/*.npy")

map = {}

features = []
count = 0

for file_index in range(len(files)):

    if file_index % 5000 == 0:
        print(str(file_index)+"\t"+str(len(files)))

    file = files[file_index]

    id = file.split("/")[-1].split(".")[0]

    try:
        file_vector = numpy.load(files[file_index])
        t.add_item(count, file_vector)
        

        features.append(file_vector)

        map[count] = id

        count += 1

    except Exception as e:
        tmp = e
        # print("err\t"+file+"\t"+str(e))

t.build(trees)
t.save('data/test.ann') # モデルを保存することも可能です。

# SQL LITEの作成

dbname = 'data/database.db'

def adapt_array(arr):
    """
    http://stackoverflow.com/a/31312102/190597 (SoulNibbler)
    """
    out = io.BytesIO()
    numpy.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())

def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return numpy.load(out)

# Converts np.array to TEXT when inserting
sqlite3.register_adapter(numpy.ndarray, adapt_array)

# Converts TEXT to np.array when selecting
sqlite3.register_converter("array", convert_array)

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
    users = []
    for index in map:
        if index % 1000 == 0:
            print(index)
        users.append((index, map[index], features[index]))
    c.executemany(sql, users)
    conn.commit()