#!/bin/bash

set -x

if [[ -d output_data ]]; then rm -rf output_data; fi

cp wrangletoc.json ~/.axiom/modules/

axiom-fleet axiom-quest -i $1

axiom-exec --fleet axiom-quest "sudo apt-get remove -y python3.8 && sudo apt-get install -y python3.9 python3.9-distutils"
axiom-exec --fleet axiom-quest "wget https://bootstrap.pypa.io/get-pip.py && python3.9 get-pip.py"
axiom-exec --fleet axiom-quest "pip3 install --upgrade requests ijson lxml tqdm aiohttp hatchling"
axiom-exec --fleet axiom-quest "git clone https://github.com/rl1987/data-analysis.git" 
axiom-exec --fleet axiom-quest "cd data-analysis && git checkout tic && cd transparency-in-coverage/python/mrfutils && pip3 install ."

axiom-scan urls.txt -m wrangletoc -o output_data
axiom-rm -f "axiom-quest*"

cp -R output_data /root/data/hospital-prices-tocfiles

branch_name="$2"
dolt checkout -b "$branch_name" 84l77v062ct099sfnm485l59778d93cc

for table in toc toc_plan toc_file toc_plan_file; do
    for f in $(ls output_data/$table.*); do 
        time -p nice -n -10 dolt table import -u "$table" --file-type=csv "$f"
    done
done

dolt add .
dolt commit -m "$branch_name"
dolt push -u origin "$branch_name"
dolt checkout main
rm -rf output_data
popd || exit
