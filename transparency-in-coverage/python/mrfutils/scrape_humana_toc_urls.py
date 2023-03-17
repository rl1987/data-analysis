#!/usr/bin/python3

import time

import requests

PER_PAGE = 100

def main():
    start_at = 0

    params = {
        'sEcho': '6',
        'iColumns': '3',
        'sColumns': ',,',
        'iDisplayStart': str(start_at),
        'iDisplayLength': str(PER_PAGE),
        'mDataProp_0': 'name',
        'sSearch_0': '',
        'bRegex_0': 'false',
        'bSearchable_0': 'false',
        'mDataProp_1': 'modifiedDate',
        'sSearch_1': '',
        'bRegex_1': 'false',
        'bSearchable_1': 'false',
        'mDataProp_2': 'sizeToDisplay',
        'sSearch_2': '',
        'bRegex_2': 'false',
        'bSearchable_2': 'false',
        'sSearch': '',
        'bRegex': 'false',
        '_': int(time.time() * 1000)
    }

    while True:
        resp = requests.get("https://developers.humana.com/syntheticdata/Resource/GetData", params=params)

        json_dict = resp.json()

        results = json_dict.get("aaData", [])

        for result_dict in results:
            name = result_dict.get("name")
            url2 = "https://developers.humana.com/syntheticdata/Resource/DownloadTOCFile?fileName=" + name
            resp2 = requests.head(url2)
            print(resp2.headers.get('Location', ""))

        if len(results) < PER_PAGE:
            break

        params['iDisplayStart'] = str(int(params['iDisplayStart']) + PER_PAGE)

if __name__ == "__main__":
    main()

