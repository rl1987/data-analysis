#!/usr/bin/python3

import random
import sys

import doltcli as dolt
import requests

CHUNK_SIZE = 256

def main():
    if len(sys.argv) != 4:
        print("Usage:")
        print("{} <pending_urls_file> <anthem_urls_file> <dolt_db_dir>".format(sys.argv[0]))
        return

    pending_urls_file = sys.argv[1]
    anthem_urls_file = sys.argv[2]
    dolt_db_dir = sys.argv[3]

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

    in_f = open(anthem_urls_file, "r")
    for url in in_f.read().strip().split('\n'):
        if not url in exclude:
            candidates.add(url)

    for url in random.sample(list(candidates), CHUNK_SIZE):
        print(url)

if __name__ == "__main__":
    main()

