from annoy import AnnoyIndex
from helper import *
import glob
from os.path import join
import numpy
import os
import json

# 初期設定

# 次元
dims = 2048

# 検索対象数
n_nearest_neighbors = 20

t = AnnoyIndex(dims, metric='angular')
t.load('data/test.ann')

# インデックスマップの読み込み（Annoyのインデックス内のIDと特徴ベクトルの対応）

file_index_map = {}
with open("data/file_index_map.json") as f:
    file_index_map = json.load(f)

# 検索クエリデータの読み込み

graph_path = join('/tmp/imagenet', 'classify_image_graph_def.pb')

query_img_path = "data/syozo-8.jpg"


# modelの読み込み
with tf.gfile.FastGFile(graph_path, 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')

with tf.Session() as sess:
    pool3 = sess.graph.get_tensor_by_name('pool_3:0')

    image_data = tf.gfile.FastGFile(query_img_path, 'rb').read()
    pool3_features = sess.run(
        pool3, {'DecodeJpeg/contents:0': image_data})
    query_feat = np.squeeze(pool3_features)

# 予測

nearest_neighbors = t.get_nns_by_vector(query_feat, n_nearest_neighbors)

for j in nearest_neighbors:
    filename_wo_ext = file_index_map[str(j)]
    '''
    neighbor_file_vector = image_vectors[filename_wo_ext]

    # 類似度計算
    similarity = 1 - \
        spatial.distance.cosine(query_feat, neighbor_file_vector)
    rounded_similarity = int((similarity * 10000)) / 10000.0
    '''

    print(filename_wo_ext)