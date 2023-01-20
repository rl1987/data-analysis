#!/usr/bin/python3

from urllib.parse import urlparse
import logging

import ijson

from mrfutils import JSONOpen

def file_name_from_mrf_url(url):
    o = urlparse(url)
    return o.path.split("/")[-1]

def main():
    log = logging.getLogger('mrfutils')
    log.setLevel(logging.WARNING)
    toc_url = "https://antm-pt-prod-dataz-nogbd-nophi-us-east1.s3.amazonaws.com/anthem/2023-01-01_anthem_index.json.gz"
    
    seen_files = dict()

    with JSONOpen(toc_url) as f:
        parser = ijson.parse(f, use_float=True)
        for prefix, event, value in parser:
            if (
                prefix.endswith('location')
                and event == 'string'
                and 'in-network' in value
            ):
                file_name = file_name_from_mrf_url(value)
                if not file_name in seen_files:
                    print(value)
                    seen_files[file_name] = True

if __name__ == "__main__":
    main()
