#!/usr/bin/python3

from glob import glob
import sys
import os

import requests
import pandas as pd

def unify(raw_output_dir, clean_output_dir, table_name):
    big_df = pd.DataFrame()

    for f in glob("{}/{}.*".format(raw_output_dir, table_name)):
        print(f)
        df = pd.read_csv(f, dtype='str')
        df.drop_duplicates(inplace=True)

        big_df = big_df.append(df)
        big_df.drop_duplicates(inplace=True)

    print(big_df)
    big_df.to_csv(os.path.join(clean_output_dir, table_name + ".csv"), index=False)

def main():
    if len(sys.argv) != 3:
        print("Usage:")
        print("{} <raw_output_dir> <clean_output_dir>".format(sys.argv[0]))
        return

    raw_output_dir = sys.argv[1]
    clean_output_dir = sys.argv[2]

    for table_name in ["code", "file", "insurer", "npi_rate", "price_metadata", "rate", "file_rate", "telemetry"]:
        print("Unifying: {}".format(table_name))
        unify(raw_output_dir, clean_output_dir, table_name)

if __name__ == "__main__":
    main()
