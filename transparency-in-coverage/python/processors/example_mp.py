#!/usr/bin/python3

# python3 example_mp.py -o "./test_out" -c quest/week0/codes_prelim.csv -n quest/week0/npis.csv -u urls_uniq.txt 

import argparse
import functools
import hashlib
import logging
import uuid
from multiprocessing import Pool
import os

from mrfutils import data_import, flatten_mrf, InvalidMRF

def perform_task(url, out_dir, code_set, npi_set):
    out_dir = make_out_dirname(out_dir, url)

    try:
        flatten_mrf(
            loc = url,
            out_dir = out_dir,
            code_set = code_set,
            npi_set = npi_set
        )
    except InvalidMRF as e:
        log.critical(e)

def make_out_dirname(out_dir, url):
    return os.path.join(out_dir, hashlib.sha1(url.encode('utf-8')).hexdigest())

def main():
    logging.basicConfig()
    log = logging.getLogger('mrfutils')
    log.setLevel(logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--out', default = 'out_dir')
    parser.add_argument('-c', '--codes')
    parser.add_argument('-n', '--npis')
    parser.add_argument('-u', '--url-list', default="urls_uniq.txt")

    args = parser.parse_args()
    out_dir = args.out
    if args.codes:
        code_set = data_import(args.codes)
    else:
        code_set = None
    if args.npis:
        npi_set = {int(x[0]) for x in data_import(args.npis)}
    else:
        npi_set = None

    in_f = open(args.url_list, "r")
    urls = in_f.read().strip().split("\n")
    in_f.close()
    
    pool = Pool(16)
    partial_perform_task = functools.partial(perform_task, out_dir=out_dir, code_set=code_set, npi_set=npi_set)
    pool.map(partial_perform_task, urls)

if __name__ == "__main__":
    main()
