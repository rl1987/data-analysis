#!/usr/bin/python3

import requests
from lxml import html

def main():
    url = "https://eusprdtransparencymrfp32.z13.web.core.windows.net/hphc"

    resp = requests.get(url)

    tree = html.fromstring(resp.text)

    for toc_url in tree.xpath('//a[contains(@href, "index.json")]/@href'):
        print(toc_url)

if __name__ == "__main__":
    main()
