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

from exceptions import InvalidMRF
from mrfutils import import_csv_to_set, json_mrf_to_csv

import requests

def process_url(url):
    output_dir_path = sys.argv[2]
    script_dir = os.path.dirname(os.path.abspath(__file__))

    code_filter = import_csv_to_set(os.path.join(script_dir, "quest/codes.csv"))
    npi_filter = import_csv_to_set(os.path.join(script_dir, "quest/npis.csv"))

    tries_left = 3
    u = str(uuid.uuid4())

    out_dir = os.path.join(output_dir_path, u)

    started_at = datetime.now().timestamp()

    try:
        resp = requests.head(url, timeout=5.0)
    except Exception as e:
        print(e)
        return

    size = resp.headers.get('Content-Length')
    
    while tries_left > 0:
        try:
            print("Starting:", url)
            json_mrf_to_csv(
                url=url,
                npi_filter=npi_filter,
                code_filter=code_filter,
                out_dir=out_dir
            )
            print("Done:", url)
            break
        except InvalidMRF:
            print("Invalid MRF at:", url)
            if os.path.isdir(out_dir):
                shutil.rmtree(out_dir)
            return
        except Exception as e:
            print(e)
            print("Failed processing MRF at: {}".format(url))
            tries_left -= 1
            if os.path.isdir(out_dir):
                shutil.rmtree(out_dir)

    done_at = datetime.now().timestamp()
    duration = done_at - started_at

    row = {
        "url": url,
        "duration": duration,
        "size": size,
        "retries": 3 - tries_left
    }

    telemetry_started = os.path.isfile(os.path.join(out_dir, "telemetry.csv", "a"))

    out_f = open(os.path.join(out_dir, "telemetry.csv"), "a", encoding="utf-8")

    csv_writer = csv.DictWriter(out_f, fieldnames = list(row.keys()), lineterminator="\n")
    if not telemetry_started:
        csv_writer.writeheader()
    csv_writer.writerow(row)

    out_f.close()

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
