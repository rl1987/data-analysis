#!/bin/bash

cp mrf2sql.json ~/.axiom/modules/

axiom-fleet axiom-quest -i 8

axiom-exec --fleet axiom-quest "sudo apt-get remove -y python3.8 && sudo apt-get install -y python3.9 python3.9-distutils"
axiom-exec --fleet axiom-quest "wget https://bootstrap.pypa.io/get-pip.py && python3.9 get-pip.py"
axiom-exec --fleet axiom-quest "pip3 install --upgrade requests ijson lxml tqdm aiohttp"
axiom-exec --fleet axiom-quest "git clone https://github.com/rl1987/data-analysis.git && cd data-analysis/ && git fetch && git checkout axiom"

# python3.9 ~/data-analysis/transparency-in-coverage/python/processors/mrf2sql.py input output

python3 example3.py -u https://antm-pt-prod-dataz-nogbd-nophi-us-east1.s3.amazonaws.com/anthem/2022-12-01_anthem_index.json.gz 
cat in_network_urls.txt | sort | uniq > urls_uniq.txt

axiom-scan urls_uniq.txt -m mrf2sql -o dump.sql

# TODO: import dump.sql into Dolt

axiom-rm -f "axiom-quest*"
