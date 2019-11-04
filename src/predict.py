import numpy
import glob
from annoy import AnnoyIndex
from scipy import spatial
import json

## メタデータのロード ##

files = glob.glob("/Users/nakamura/git/d_jps/cj/src/*/data/list.json")
map = {}
for file in files:
    print(file)
    with open(file) as f:
        df = json.load(f)
    for obj in df:
        id = obj["_id"].split("/")[-1].split("#")[0]
        map[id] = obj

##　Indexの読み込み　##

file_index_map = {}
with open("file_index_map.json") as f:
    file_index_map = json.load(f)

########

# config
dims = 2048

t = AnnoyIndex(dims)
t.load('test.ann') # モデルを読み込むことも可能です。

########

n_nearest_neighbors = 200

image_vectors_path = "output/image_vectors"
files = glob.glob(image_vectors_path+"/*.npy")

for file_index in range(len(files)):

    file = files[file_index]

    master_vector = numpy.load(file)

    nearest_neighbors = t.get_nns_by_vector(master_vector, n_nearest_neighbors)
    
    id = file.split("/")[-1].split(".")[0]

    arr = []

    for j in nearest_neighbors:

        neighbor_file_name = file_index_map[str(j)]

        '''

        neighbor_file_vector = numpy.load(XXX)

        similarity = 1 - \
            spatial.distance.cosine(master_vector, neighbor_file_vector)
        rounded_similarity = int((similarity * 10000)) / 10000.0

        arr.append(obj)
        '''

        id2 = neighbor_file_name.split(".")[0]
        if id2 not in map:
            print("- "+id2)
            continue
        
        obj2 = map[id2]

        obj = {
            "id" : id2,
            # "score": rounded_similarity,
            "thumbnail": obj2["image"],
            "title": obj2["label"],
            # "sourceInfo": obj2["sourceInfo"],
            "accessInfo": obj2["accessInfo"]
        }

        arr.append(obj)

    f2 = open('../data/'+id+'.json', 'w')
    json.dump(arr, f2)