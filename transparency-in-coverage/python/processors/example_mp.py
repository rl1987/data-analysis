#!/usr/bin/python3

# python3 example_mp.py -c quest/codes.csv -n quest/npis.csv

import argparse
import functools
import hashlib
import logging
import uuid
from multiprocessing import Pool
import os
from urllib.parse import urlparse

from mrfutils import import_csv_to_set, json_mrf_to_csv, InvalidMRF, _filename_hash
from idxutils import get_unique_in_network_urls 

import mysql.connector as connector

def perform_task(url, code_set, npi_set):
    # https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
    cnx = connector.connect(user='rl', password='trustno1', host='127.0.0.1', database='quest')

    try:
        json_mrf_to_csv(
            loc = url,
            cnx = cnx,
            out_dir = None,
            code_filter = code_set,
            npi_filter = npi_set
        )
    except InvalidMRF as e:
        logging.critical(e)
    except Exception as e:
        logging.critical(e)

def file_not_taken(cnx, url):
    fh = _filename_hash(url)

    cursor = cnx.cursor()

    sql = 'SELECT COUNT(*) FROM `plans_files` WHERE `filename_hash` = "{}";'.format(fh)
    
    logging.debug(sql)
    cursor.execute(sql)
    count = cursor.fetchone()[0]
    cursor.close()

    return count == 0

def main():
    logging.basicConfig()
    log = logging.getLogger('mrfutils')
    log.setLevel(logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--codes')
    parser.add_argument('-n', '--npis')
    parser.add_argument('-p', '--pool-size', type=int, default=16)

    args = parser.parse_args()
    if args.codes:
        code_set = import_csv_to_set(args.codes)
    else:
        code_set = None
    if args.npis:
        npi_set = {int(x[0]) for x in import_csv_to_set(args.npis)}
    else:
        npi_set = None

    # https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
    cnx = connector.connect(user='rl', password='trustno1', host='127.0.0.1', database='quest')

    urls = get_unique_in_network_urls('https://antm-pt-prod-dataz-nogbd-nophi-us-east1.s3.amazonaws.com/anthem/2022-12-01_anthem_index.json.gz')

    logging.info("Got {} MRF URLs - filtering".format(len(urls)))
    urls = list(filter(file_not_taken, urls))
    logging.info("Got {} MRF URLs after filtering".format(len(urls)))

    cnx.close()

    pool = Pool(args.pool_size)
    partial_perform_task = functools.partial(perform_task, code_set=code_set, npi_set=npi_set)
    pool.map(partial_perform_task, urls)

if __name__ == "__main__":
    main()
