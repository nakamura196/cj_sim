import json
from SPARQLWrapper import SPARQLWrapper
import urllib.parse
import requests
import csv
import os
import time
import sys
import argparse

import requests
import shutil

def download_img(url, file_name):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(file_name, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    else:
        with open(file_name.replace(".jpg", ".txt"), mode='w') as f:
                f.write("")
        print("err\t"+file_name)


list_path = '/Users/nakamura/git/d_jps/cj/src/js/data/list.json'

with open(list_path) as f:
    df = json.load(f)

for i in range(len(df)):
    obj = df[i]

    url = obj["image"]

    name = obj["_id"].split("/")[-1].split("#")[0]

    if i % 100 == 0:
        print(str(i+1)+"/"+str(len(df))+"\t"+name)

    if "dignl" in url or "issnl" in url:
        continue

    if url == "":
        continue

    dir = name.split("-")[0]

    opath = "/Users/nakamura/git/thumbnail/"+dir+"/"+name+".jpg"

    if os.path.exists(opath) or os.path.exists(opath.replace(".jpg", ".txt")):
        continue

    if "data.ukiyo-e.org/metro/scaled" in url:
        with open(opath.replace(".jpg", ".txt"), mode='w') as f:
                f.write("")
        print("err\t"+opath)
        continue

    try:
        print(url)
        download_img(url, opath)
    except:
        time.sleep(0.01)
        with open(opath.replace(".jpg", ".txt"), mode='w') as f:
                f.write("")
        print("err\t"+opath)
