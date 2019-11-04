import json
import boto3
import glob
import csv

bucket_name = "cultural-jp"
s3 = boto3.resource('s3')

files = glob.glob("../docs/json/*.json")

for i in range(len(files)):
    file = files[i]
    print(i)
    print(len(files))
    print("---")

    filename = file.split("/")[-1]

    try:
        s3.Bucket(bucket_name).upload_file(
            file, "json/"+filename)
    except:
        print("Error")
