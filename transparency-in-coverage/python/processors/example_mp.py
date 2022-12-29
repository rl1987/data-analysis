#!/usr/bin/python3

# python3 example_mp.py -c quest/week0/codes_prelim.csv -n quest/week0/npis.csv

import argparse
import functools
import hashlib
import logging
import uuid
from multiprocessing import Pool
import os

from mrfutils import import_csv_to_set, json_mrf_to_csv, InvalidMRF
from idxutils import gen_in_network_links

import mysql.connector as connector

def perform_task(url, code_set, npi_set):
    # https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
    cnx = connector.connect(user='rl', password='trustno1', host='127.0.0.1', database='quest')

    try:
        json_mrf_to_csv(
            loc = url,
            cnx = cnx,
            code_filter = code_set,
            npi_filter = npi_set
        )
    except InvalidMRF as e:
        log.critical(e)
    except Exception as e:
        log.critical(e)

def get_urls(toc_url):
    seen_urls = dict()

    for url in gen_in_network_links(toc_url):
        seen_urls[url] = True

    return list(seen_urls.keys())

def main():
    logging.basicConfig()
    log = logging.getLogger('mrfutils')
    log.setLevel(logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--codes')
    parser.add_argument('-n', '--npis')

    args = parser.parse_args()
    if args.codes:
        code_set = import_csv_to_set(args.codes)
    else:
        code_set = None
    if args.npis:
        npi_set = {int(x[0]) for x in import_csv_to_set(args.npis)}
    else:
        npi_set = None

    urls = get_urls('https://antm-pt-prod-dataz-nogbd-nophi-us-east1.s3.amazonaws.com/anthem/2022-12-01_anthem_index.json.gz')
    urls = urls[:16] # TODO: remove this when it works good on small scale

    pool = Pool(16)
    partial_perform_task = functools.partial(perform_task, code_set=code_set, npi_set=npi_set)
    pool.map(partial_perform_task, urls)

if __name__ == "__main__":
    main()
