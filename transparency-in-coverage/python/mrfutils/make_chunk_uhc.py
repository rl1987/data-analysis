#!/usr/bin/python3

import sys

import doltcli as dolt
import requests

CHUNK_SIZE = 128

def main():
    if len(sys.argv) != 2:
        print("Usage:")
        print("{} <dolt_db_dir>".format(sys.argv[0]))
        return

    dolt_db_dir = sys.argv[1]

    exclude = set()

    db = dolt.Dolt(dolt_db_dir)
    sql = 'SELECT DISTINCT(url) FROM file WHERE url IS NOT NULL;'
    
    try:
        res = db.sql(sql, result_format="json")
        for row in res['rows']:
            exclude.add(row.get('url)'))
    except:
        pass

    candidates = []

    resp = requests.get("https://transparency-in-coverage.uhc.com/api/v1/uhc/blobs/")

    for blob_dict in resp.json().get("blobs"):
        url = blob_dict.get("downloadUrl")
        if not "in-network" in url:
            continue
        size = blob_dict.get("size")

        if not url in exclude:
            candidates.append((url, size))
    
    candidates = sorted(candidates, key=lambda t: t[1], reverse=True)
    
    if len(candidates) > CHUNK_SIZE:
        candidates = candidates[:CHUNK_SIZE]

    for c in candidates:
        print(c[0])

if __name__ == "__main__":
    main()

