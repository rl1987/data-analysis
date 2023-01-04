#!/bin/bash

curl "https://transparency-in-coverage.uhc.com/api/v1/uhc/blobs/" | jq -r ".blobs[].downloadUrl" | grep in-network > urls.txt
