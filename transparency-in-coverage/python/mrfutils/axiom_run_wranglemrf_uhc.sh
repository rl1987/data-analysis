#!/bin/bash

set -x

if [[ -d output_data ]]; then rm -rf output_data; fi
if [[ -d raw_output_data ]]; then rm -rf raw_output_data; fi

pushd /root/data/quest-v4 || exit
dolt checkout main
dolt remote add upstream dolthub/quest-v4
dolt pull upstream
dolt push
popd || exit

cp wranglemrf.json ~/.axiom/modules/

python3 get_pending_mrf_urls.py | anew > pending.txt
python3 make_chunk_uhc.py pending.txt /root/data/quest-v4 > urls.txt

axiom-fleet axiom-quest -i 64

axiom-exec --fleet axiom-quest "sudo apt-get remove -y python3.8 && sudo apt-get install -y python3.9 python3.9-distutils"
axiom-exec --fleet axiom-quest "wget https://bootstrap.pypa.io/get-pip.py && python3.9 get-pip.py"
axiom-exec --fleet axiom-quest "pip3 install --upgrade requests ijson lxml tqdm aiohttp"
axiom-exec --fleet axiom-quest "git clone https://github.com/rl1987/data-analysis.git && cd data-analysis/ && git fetch && git checkout quest_v4_bounty"

axiom-scan urls.txt -m wranglemrf -o raw_output_data
axiom-rm -f "axiom-quest*"

mkdir output_data
python3 unify_csv_files.py raw_output_data output_data

cp -R output_data /root/data/quest-v4
pushd /root/data/quest-v4 || exit
dolt checkout main
dolt pull upstream 
dolt push

for table in file insurer code price_metadata rate tin tin_rate_file npi_tin; do
    for f in $(ls output_data/$table.*); do 
        time -p nice -n -10 dolt table import -u "$table" --file-type=csv "$f"
    done
done

branch_name=$(date --rfc-3339=seconds | sed 's/://g' | sed 's/\s/__/g' | sed 's/-/_/g' | cut -f1 -d '+')
dolt checkout -b "$branch_name" vqbnk0gdv2lhsuvfoc142bg4q8023i1t
dolt add .
dolt commit -m "UHC data"
dolt push -u origin "$branch_name"
dolt checkout main
rm -rf output_data
popd || exit
