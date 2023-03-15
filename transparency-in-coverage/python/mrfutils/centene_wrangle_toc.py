#!/usr/bin/python3

from urllib.parse import urljoin

import requests
from lxml import html

from mrfutils import toc_file_to_csv

def main():
    resp = requests.get("https://www.centene.com/price-transparency-files.html")
    tree = html.fromstring(resp.text)
    for idx_link in tree.xpath('//a[starts-with(@href, "/content/dam/centene")]/@href'):
        idx_url = urljoin(resp.url, idx_link)
        toc_file_to_csv(url=idx_url, out_dir="centene_toc")

if __name__ == "__main__":
    main()

