#!/usr/bin/python3

from urllib.parse import urljoin

import requests
from lxml import html

from mrfutils.helpers import JSONOpen

def gen_in_network_links(index_loc,):
    """
    Gets in-network files from index.json files
    :param index.json URL:
    """
    with JSONOpen(index_loc) as f:
        count = 0
        parser = ijson.parse(f, use_float=True)
        for prefix, event, value in parser:
            if (
                prefix.endswith('location')
                and event == 'string'
                and 'in-network' in value
            ):
                yield value

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

