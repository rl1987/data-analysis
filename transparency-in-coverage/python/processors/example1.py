#!/usr/bin/python3

import logging
from pathlib import Path

from tqdm.contrib.logging import logging_redirect_tqdm
from tqdm import tqdm

from exporters import SQLDumpExporter
from mrfutils import import_csv_to_set, json_mrf_to_csv, InvalidMRF

log = logging.getLogger("mrfutils")

code_filter = import_csv_to_set("test/codes.csv")
npi_filter = import_csv_to_set("test/npis.csv")

p = Path(__file__).parent.absolute()

in_f = open("urls_uniq.txt", "r")
urls = in_f.read().strip().split('\n')
in_f.close()

exporter = SQLDumpExporter("dump.sql")
exporter.start()

for url in tqdm(urls):
    with logging_redirect_tqdm():
        try:
            json_mrf_to_csv(
                loc=url,
                url=url,
                npi_filter=npi_filter,
                code_filter=code_filter,
                exporter=exporter,
            )
        except InvalidMRF:
            log.warning("Not a valid MRF.")

exporter.finalise()
