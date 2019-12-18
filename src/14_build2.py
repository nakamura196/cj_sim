import numpy
import glob
from annoy import AnnoyIndex
from scipy import spatial
import json

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
    # print(file_index)

    if file_index % 5000 == 0:
        print(str(file_index)+"\t"+str(len(files)))

    file = files[file_index]

    id = file.split("/")[-1].split(".")[0]

    try:
        file_vector = numpy.load(files[file_index])
        t.add_item(file_index, file_vector)
        

        features.append(file_vector)

        map[count] = id

        count += 1

    except:
        print("err\t"+file)

t.build(trees)
t.save('data/test.ann') # モデルを保存することも可能です。

n_nearest_neighbors = 20

result = {}

for file_index in map:
    file_vector = features[file_index]

    nearest_neighbors = t.get_nns_by_vector(file_vector, n_nearest_neighbors)

    arr = []

    id = map[file_index]

    for j in nearest_neighbors:

        id2 = map[j]
        arr.append(id2)

    result[id] = arr


'''
f2 = open('data/file_index_map.json', 'w')
json.dump(map, f2)

numpy.save('data/features.npy', features)
'''

f2 = open('data/result.json', 'w')
json.dump(result, f2)