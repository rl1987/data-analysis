#!/usr/bin/python3

import os
import sys

import requests

from mrfutils import toc_file_to_csv

def main():
    resp = requests.get("https://transparency-in-coverage.uhc.com/api/v1/uhc/blobs/")

    for blob_dict in resp.json().get("blobs"):
        url = blob_dict.get("downloadUrl")
        if not "index" in url:
            continue

        print(url)

        toc_file_to_csv(url=url, out_dir="uhc_toc")

if __name__ == "__main__":
    main()

