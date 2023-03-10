#!/usr/bin/python3

import sys

import requests

def main():
    candidates = []

    resp = requests.get("https://transparency-in-coverage.uhc.com/api/v1/uhc/blobs/")

    for blob_dict in resp.json().get("blobs"):
        url = blob_dict.get("downloadUrl")
        if "index" in url:
            candidates.append(url)

    candidates = sorted(candidates, key=lambda t: t[1], reverse=True)
    
    for url in candidates:
        print(url)

if __name__ == "__main__":
    main()

