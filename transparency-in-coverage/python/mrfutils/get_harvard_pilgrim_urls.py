#!/usr/bin/python3

import requests
from lxml import html

from idxutils import *

def main():
    page_url = "https://eusprdtransparencymrfp32.z13.web.core.windows.net/hphc"

    resp = requests.get(page_url)

    tree = html.fromstring(resp.text)

    out_f = open("urls.txt", "w")

    for index_url in tree.xpath('//a[contains(@href, "index.json")]/@href'):
        for url in gen_in_network_links(index_url):
            if url.endswith(".zip"):
                continue

            print(url)
            out_f.write(url + "\n")

    out_f.close()

if __name__ == "__main__":
    main()

