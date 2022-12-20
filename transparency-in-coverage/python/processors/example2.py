import ijson
from mrfutils import MRFOpen

def mrfs_from_idx(index_loc):
    """
    Gets in-network files from index.json files
    :param idx_url:
    :return: list of in-network file URLS
    """
    in_network_file_urls = []
    with MRFOpen(index_loc) as f:
        parser = ijson.parse(f, use_float=True)
        for prefix, event, value in parser:
            if (
                prefix.endswith('location')
                and event == 'string'
                and 'in-network' in value
            ):
                yield value

index_loc = 'https://antm-pt-prod-dataz-nogbd-nophi-us-east1.s3.amazonaws.com/anthem/2022-12-01_anthem_index.json.gz'
for url in mrfs_from_idx(index_loc):
    print(url)
