#!/usr/bin/python3

from urllib.parse import urljoin

import ijson
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
    page_url = "https://files.hfbenefits.com/transparancy-in-coverage/0070900"

    resp = requests.get(page_url)

    tree = html.fromstring(resp.text)

    out_f = open("urls.txt", "w")

    for index_url in tree.xpath('//a[contains(@href, "index.json")]/@href'):
        index_url = urljoin(resp.url, index_url)
        for url in gen_in_network_links(index_url):
            if url.endswith(".zip"):
                continue

            print(url)
            out_f.write(url + "\n")

    out_f.close()

if __name__ == "__main__":
    main()

