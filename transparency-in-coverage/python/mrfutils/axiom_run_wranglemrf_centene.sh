#!/bin/bash

# FIXME: code duplication with axiom_run_wranglemrf.sh

set -x

if [[ -d output_data ]]; then rm -rf output_data; fi

pushd /root/data/quest-v3 || exit
dolt checkout main
dolt remote add upstream dolthub/quest-v3
dolt pull upstream
dolt push
popd || exit

cp wranglemrf.json ~/.axiom/modules/

python3 centene_get_mrf_urls.py

axiom-fleet axiom-quest -i 16

axiom-exec --fleet axiom-quest "sudo apt-get remove -y python3.8 && sudo apt-get install -y python3.9 python3.9-distutils"
axiom-exec --fleet axiom-quest "wget https://bootstrap.pypa.io/get-pip.py && python3.9 get-pip.py"
axiom-exec --fleet axiom-quest "pip3 install --upgrade requests ijson lxml tqdm aiohttp"
axiom-exec --fleet axiom-quest "git clone https://github.com/rl1987/data-analysis.git && cd data-analysis/ && git fetch && git checkout quest_v3_bounty"

axiom-scan urls.txt -m wranglemrf -o output_data
axiom-rm -f "axiom-quest*"

cp -R output_data /root/data/quest-v3
pushd /root/data/quest-v3 || exit
dolt checkout main
dolt pull upstream 
dolt push

for table in file insurer code price_metadata rate npi_rate; do
    for f in $(ls output_data/$table.*); do 
        time -p nice -n -10 dolt table import -u "$table" --file-type=csv "$f"
    done
done

branch_name="centene"
dolt checkout -b "$branch_name"
dolt add .
dolt commit -m "Centene data"
dolt push -u origin "$branch_name"
dolt checkout main
rm -rf output_data
popd || exit
