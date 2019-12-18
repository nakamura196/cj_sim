import json
import boto3
import glob
import csv
import time

bucket_name = "cultural-jp"
s3 = boto3.resource('s3')

files = glob.glob("../data/*.json")

path_w = 'data/uploaded_list_json.csv'

rows = []

with open(path_w, 'r') as f:
    reader = csv.reader(f)
    # header = next(reader)  # ヘッダーを読み飛ばしたい時

    for row in reader:
        rows.append(row[0])

d = 20

for i in range(len(files)):
    file = files[i]

    filename = file.split("/")[-1]

    url = "https://nakamura196.github.io/cj2/#/item?id="+filename.replace(".json", "")

    # if i % d == 0:
    print(str(i+1)+"/"+str(len(files))+"\t"+url)

    

    if filename not in rows:

        try:
            s3.Bucket(bucket_name).upload_file(
                file, "json/"+filename)

            rows.append(filename)

            if len(rows) % d == 0:
                with open(path_w, 'w') as f:
                    writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
                    for line in rows:
                        writer.writerow([line])

        except:
            time.sleep(0.5)
            print("Error")
