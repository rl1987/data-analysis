#!/usr/bin/python3

import random

import requests

def main():
    resp = requests.get("https://transparency-in-coverage.optum.com/api/v1/oh/blobs/")

    for blob_dict in resp.json().get("blobs"):
        url = blob_dict.get("downloadUrl")
        if url is not None and "in-network" in url:
            print(url)

if __name__ == "__main__":
    main()

