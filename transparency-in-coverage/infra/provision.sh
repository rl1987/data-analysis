#!/bin/bash

set -x

apt-get update
apt-get install -y python3 python3-pip tmux git vim visidata unzip jq default-libmysqlclient-dev

curl -L https://github.com/dolthub/dolt/releases/latest/download/install.sh > /tmp/install.sh && bash /tmp/install.sh
dolt config --global --add user.email rimantas@keyspace.lt
dolt config --global --add user.name "rl1987"

pip3 install --upgrade requests aiohttp ijson lxml tqdm mysql-connector-python

useradd do-agent --no-create-home --system
curl -sSL https://repos.insights.digitalocean.com/install.sh -o /tmp/install.sh
bash /tmp/install.sh

mkdir /root/data

pushd /root/data || exit
dolt clone rl1987/quest
popd || exit

mkdir /root/src

pushd /root/src || exit
git clone https://github.com/rl1987/data-analysis.git
popd || exit

pushd /root/src/data-analysis/transparency-in-coverage/python/processors || exit
wget https://antm-pt-prod-dataz-nogbd-nophi-us-east1.s3.amazonaws.com/anthem/2022-12-01_anthem_index.json.gz
popd || exit

curl -fsSL https://deb.nodesource.com/setup_18.x -o /tmp/install_node.sh
bash /tmp/install_node.sh
apt-get install -y gcc g++ make nodejs

npm install pm2 -g

sudo pm2 start 'dolt sql-server --data-dir /root/data -H 127.0.0.1 --user=rl --password=trustno1 --loglevel=trace'
pm2 save
pm2 startup systemd
