#!/usr/bin/python3

import csv
from glob import glob
import os
import tempfile
import sys
import shutil

from exporters import SQLDumpExporter
from mrfutils import import_csv_to_set, json_mrf_to_csv

def convert_csv_to_sql(csv_dir, output_file_path):
    exporter = SQLDumpExporter(output_file_path)
    exporter.start()
    
    for f in glob(csv_dir + "/*.csv"):
        tablename = f.split('/')[-1].replace('.csv', '')

        in_f = open(f, "r")
        
        csv_reader = csv.DictReader(in_f)
        for row in csv_reader:
            exporter.write_row(tablename, row)
            
        in_f.close()

    exporter.finalise()

def main():
    if len(sys.argv) != 3:
        print("Usage:")
        print("{} <input_file_path> <output_file_path>".format(sys.argv[0]))
        return 0

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    in_f = open(input_file_path, "r")
    urls = in_f.read().strip().split("\n")
    in_f.close()

    script_dir = os.path.dirname(os.path.abspath(__file__))

    code_filter = import_csv_to_set(os.path.join(script_dir, "quest/codes.csv"))
    npi_filter = import_csv_to_set(os.path.join(script_dir, "quest/npis.csv"))

    tmp_out_dir = tempfile.mkdtemp()

    for url in urls:
        try:
            print("Starting:", url)
            json_mrf_to_csv(
                url=url,
                npi_filter=npi_filter,
                code_filter=code_filter,
                out_dir=tmp_out_dir
            )
            print("Done:", url)
        except Exception as e:
            print(e)
            print("Failed processing MRF at: {}".format(url))
 
    convert_csv_to_sql(tmp_out_dir, output_file_path)

    shutil.rmtree(tmp_out_dir)


if __name__ == "__main__":
    main()
