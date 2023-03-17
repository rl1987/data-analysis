#!/usr/bin/python3

import csv
from datetime import datetime
from glob import glob
import os
import sys
import shutil
import uuid
from multiprocessing import Pool
import multiprocessing

from mrfutils.flatteners import toc_file_to_csv

import requests

def process_url(url):
    output_dir_path = sys.argv[2]
    script_dir = os.path.dirname(os.path.abspath(__file__))

    tries_left = 3
    u = str(uuid.uuid4())

    out_dir = os.path.join(output_dir_path, u)

    started_at = datetime.now().timestamp()

    try:
        resp = requests.head(url, timeout=5.0)
    except Exception as e:
        print(e)
        return

    while tries_left > 0:
        try:
            print("Starting:", url)
            toc_file_to_csv(url=url, out_dir=out_dir)
            print("Done:", url)
            break
        except Exception as e:
            print(e)
            print("Failed processing TOC at: {}".format(url))
            tries_left -= 1
            if os.path.isdir(out_dir):
                shutil.rmtree(out_dir)

def main():
    if len(sys.argv) != 3:
        print("Usage:")
        print("{} <input_file_path> <output_dir_path>".format(sys.argv[0]))
        return 0

    input_file_path = sys.argv[1]

    in_f = open(input_file_path, "r")
    urls = in_f.read().strip().split("\n")
    in_f.close()

    pool = Pool(multiprocessing.cpu_count())
    pool.map(process_url, urls)

if __name__ == "__main__":
    main()
