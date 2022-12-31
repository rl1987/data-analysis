#!/usr/bin/python3

import os
import sys

from exporters import SQLDumpExporter
from mrfutils import import_csv_to_set, json_mrf_to_csv, InvalidMRF

def main():
    if len(sys.argv) != 3:
        print("Usage:")
        print("{} <input_file_path> <output_file_path>".format(sys.argv[0]))
        return 0
    
    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    in_f = open(input_file_path, "r")
    urls = in_f.read().strip().split('\n')
    in_f.close()

    script_dir = os.path.dirname(os.path.abspath(__file__))

    code_filter = import_csv_to_set(os.path.join(script_dir,
                                                 "test/codes.csv"))
    npi_filter = import_csv_to_set(os.path.join(script_dir,
                                                "test/npis.csv"))

    exporter = SQLDumpExporter(output_file_path)
    exporter.start()

    for url in urls:
        try:
            print("Starting:", url)
            json_mrf_to_csv(
                loc=url,
                url=url,
                npi_filter=npi_filter,
                code_filter=code_filter,
                exporter=exporter,
            )
            print("Done:", url)
        except InvalidMRF:
            print("Not a valid MRF at: {}".format(url))

    exporter.finalise()

if __name__ == "__main__":
    main()

