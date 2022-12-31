#!/bin/bash

set -x

apt-get update
apt-get install -y python3 python3-pip tmux git vim visidata unzip jq

curl -L https://github.com/dolthub/dolt/releases/latest/download/install.sh > /tmp/install.sh && bash /tmp/install.sh
dolt config --global --add user.email rimantas@keyspace.lt
dolt config --global --add user.name "rl1987"

pip3 install --upgrade requests ijson lxml tqdm aiohttp

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

pushd /root || exit
wget https://raw.githubusercontent.com/pry0cc/axiom/master/interact/axiom-configure
chmod +x axiom-configure
DEBIAN_FRONTEND=noninteractive printf "\n1\nn\ndo\ny\n$(cat do_token.txt)\nsfo3\n\n\n\n\nquest\nbarebones\n\n" | ./axiom-configure
popd || exit
