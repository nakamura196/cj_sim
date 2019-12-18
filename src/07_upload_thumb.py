import json
import boto3
import glob
import csv
import time

bucket_name = "cultural-jp"
s3 = boto3.resource('s3')

files = glob.glob("../images/europeana-*.jpg")

path_w = 'data/uploaded_list_thumb.csv'

rows = []

with open(path_w, 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  # ヘッダーを読み飛ばしたい時

    for row in reader:
        rows.append(row[0])

for i in range(len(files)):
    file = files[i]
    print(i)
    print(len(files))
    print("---")

    filename = file.split("/")[-1]

    if filename in rows:
        continue

    try:
        s3.Bucket(bucket_name).upload_file(
            file, filename)

        with open(path_w, mode='a') as f:
            f.write(filename+"\n")
    except:
        time.sleep(0.5)
        print("Error")
