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

with open('/Users/nakamura/git/d_jps/cj/src/cobas/data/list.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  # ヘッダーを読み飛ばしたい時

    count = 1

    for row in reader:
        uri = row[0]

        name = uri.split("/")[-1]
        print(str(count)+"\t"+name)

        count += 1

        opath = "../images/"+name+".jpg"

        if os.path.exists(opath):
            continue

        try:

            endpoint = "https://jpsearch.go.jp/rdf/sparql"

            # time.sleep(0)

            sparql = SPARQLWrapper(endpoint=endpoint, returnFormat='json')
            q = ("""
                DESCRIBE <"""+uri+""">
            """)
            sparql.setQuery(q)

            url = endpoint+"?query="+urllib.parse.quote(q)+"&format=json&output=json&results=json"

            r = requests.get(url)
            results = json.loads(r.text)["results"]["bindings"]

            for obj in results:
                if obj["p"]["value"] == "http://schema.org/image":
                    url = obj["o"]["value"]

                    download_img(url, opath)

                    break
        
        except:
            time.sleep(0.5)
            print("Error")
