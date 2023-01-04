#!/bin/bash

set -x

cp mrf2sql.json ~/.axiom/modules/

python3 example3.py -u "$1"
cat in_network_urls.txt | sort | uniq > urls_uniq.txt

axiom-fleet axiom-quest -i $(wc -l urls_uniq.txt)

axiom-exec --fleet axiom-quest "sudo apt-get remove -y python3.8 && sudo apt-get install -y python3.9 python3.9-distutils"
axiom-exec --fleet axiom-quest "wget https://bootstrap.pypa.io/get-pip.py && python3.9 get-pip.py"
axiom-exec --fleet axiom-quest "pip3 install --upgrade requests ijson lxml tqdm aiohttp"
axiom-exec --fleet axiom-quest "git clone https://github.com/rl1987/data-analysis.git && cd data-analysis/ && git fetch && git checkout axiom"

axiom-scan urls_uniq.txt -m mrf2sql -o dump.sql
axiom-rm -f "axiom-quest*"

cp dump.sql ~/data/quest/
pushd ~/data/quest || exit
cat dump.sql | dolt sql
popd || exit
