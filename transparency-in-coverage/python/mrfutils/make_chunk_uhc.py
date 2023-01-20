#!/usr/bin/python3

import random
import sys

import doltcli as dolt
import requests

CHUNK_SIZE = 128

def main():
    if len(sys.argv) != 3:
        print("Usage:")
        print("{} <pending_urls_file> <dolt_db_dir>".format(sys.argv[0]))
        return

    pending_urls_file = sys.argv[1]
    dolt_db_dir = sys.argv[2]

    exclude = set()

    in_f = open(pending_urls_file, "r")
    for url in in_f.read().strip().split("\n"):
        exclude.add(url)
    in_f.close()

    db = dolt.Dolt(dolt_db_dir)
    sql = 'SELECT DISTINCT(url) FROM file WHERE url IS NOT NULL;'

    res = db.sql(sql, result_format="json")
    for row in res['rows']:
        exclude.add(row.get('url)'))

    candidates = set()

    resp = requests.get("https://transparency-in-coverage.uhc.com/api/v1/uhc/blobs/")

    for blob_dict in resp.json().get("blobs"):
        url = blob_dict.get("downloadUrl")
        if not "in-network" in url:
            continue

        if not url in exclude:
            candidates.add(url)

    for url in random.sample(list(candidates), CHUNK_SIZE):
        print(url)

if __name__ == "__main__":
    main()

