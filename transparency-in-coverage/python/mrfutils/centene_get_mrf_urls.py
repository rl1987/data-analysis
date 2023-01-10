#!/usr/bin/python3

from urllib.parse import urljoin

import requests
from lxml import html

from idxutils import gen_in_network_links

def main():
    out_f = open("urls.txt", "w")

    resp = requests.get("https://www.centene.com/price-transparency-files.html")
    tree = html.fromstring(resp.text)
    for idx_link in tree.xpath('//a[starts-with(@href, "/content/dam/centene")]/@href'):
        idx_url = urljoin(resp.url, idx_link)
        for mrf_url in gen_in_network_links(idx_url):
            out_f.write(mrf_url + "\n")

    out_f.close()

if __name__ == "__main__":
    main()

