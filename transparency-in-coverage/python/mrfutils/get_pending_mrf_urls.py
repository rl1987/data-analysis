#!/usr/bin/python3

import requests

def gen_mrf_urls(pull_id):
    json_data = {
        'operationName': 'PullDiffForTableList',
        'variables': {
            'ownerName': 'dolthub',
            'repoName': 'quest',
            'pullId': pull_id,
        },
        'query': 'query PullDiffForTableList($ownerName: String!, $repoName: String!, $pullId: String!) {\n  pullCommitDiff(repoName: $repoName, ownerName: $ownerName, pullId: $pullId) {\n    ...CommitDiffForTableList\n    __typename\n  }\n}\n\nfragment CommitDiffForTableList on CommitDiff {\n  _id\n  toOwnerName\n  toRepoName\n  toCommitId\n  fromOwnerName\n  fromRepoName\n  fromCommitId\n  tableDiffs {\n    ...TableDiffForTableList\n    __typename\n  }\n  __typename\n}\n\nfragment TableDiffForTableList on TableDiff {\n  oldTable {\n    ...TableForDiffTableList\n    __typename\n  }\n  newTable {\n    ...TableForDiffTableList\n    __typename\n  }\n  numChangedSchemas\n  rowDiffColumns {\n    ...ColumnForDiffTableList\n    __typename\n  }\n  rowDiffs {\n    ...RowDiffListForTableList\n    __typename\n  }\n  schemaDiff {\n    ...SchemaDiffForTableList\n    __typename\n  }\n  schemaPatch\n  __typename\n}\n\nfragment TableForDiffTableList on Table {\n  tableName\n  columns {\n    ...ColumnForDiffTableList\n    __typename\n  }\n  __typename\n}\n\nfragment ColumnForDiffTableList on Column {\n  name\n  isPrimaryKey\n  type\n  constraints {\n    notNull\n    __typename\n  }\n  __typename\n}\n\nfragment RowDiffListForTableList on RowDiffList {\n  list {\n    ...RowDiffForTableList\n    __typename\n  }\n  nextPageToken\n  filterByRowTypeRequest {\n    pageToken\n    filterByRowType\n    __typename\n  }\n  __typename\n}\n\nfragment RowDiffForTableList on RowDiff {\n  added {\n    ...RowForTableList\n    __typename\n  }\n  deleted {\n    ...RowForTableList\n    __typename\n  }\n  __typename\n}\n\nfragment RowForTableList on Row {\n  columnValues {\n    ...ColumnValueForTableList\n    __typename\n  }\n  __typename\n}\n\nfragment ColumnValueForTableList on ColumnValue {\n  displayValue\n  __typename\n}\n\nfragment SchemaDiffForTableList on TextDiff {\n  leftLines {\n    ...SchemaDiffLineForTableList\n    __typename\n  }\n  rightLines {\n    ...SchemaDiffLineForTableList\n    __typename\n  }\n  __typename\n}\n\nfragment SchemaDiffLineForTableList on Line {\n  content\n  lineNumber\n  type\n  __typename\n}\n',
    }

    resp0 = requests.post('https://www.dolthub.com/graphql', json=json_data)

    next_page_token = None

    for td in resp0.json().get("data", dict()).get("pullCommitDiff", dict()).get("tableDiffs", []):
        if td.get("oldTable", dict()).get("tableName") != "files":
            continue

        next_page_token = td.get("rowDiffs", dict()).get("nextPageToken")

        for rd in td.get("rowDiffs", dict()).get("list", []):
            if len(rd.get("added")) == 0:
                continue

            yield rd.get("added").get("columnValues")[-1].get("displayValue")

    if next_page_token is None:
        return

    json_data = {
        'operationName': 'NextPageRowDiffs',
        'variables': {
            'pageToken': next_page_token
        },
        'query': 'query NextPageRowDiffs($pageToken: String!, $filterByRowType: DiffRowType) {\n  rowDiffs(pageToken: $pageToken, filterByRowType: $filterByRowType) {\n    ...RowDiffListForTableList\n    __typename\n  }\n}\n\nfragment RowDiffListForTableList on RowDiffList {\n  list {\n    ...RowDiffForTableList\n    __typename\n  }\n  nextPageToken\n  filterByRowTypeRequest {\n    pageToken\n    filterByRowType\n    __typename\n  }\n  __typename\n}\n\nfragment RowDiffForTableList on RowDiff {\n  added {\n    ...RowForTableList\n    __typename\n  }\n  deleted {\n    ...RowForTableList\n    __typename\n  }\n  __typename\n}\n\nfragment RowForTableList on Row {\n  columnValues {\n    ...ColumnValueForTableList\n    __typename\n  }\n  __typename\n}\n\nfragment ColumnValueForTableList on ColumnValue {\n  displayValue\n  __typename\n}\n'
    }

    while next_page_token is not None:
        json_data['variables']['pageToken'] = next_page_token
        resp = requests.post('https://www.dolthub.com/graphql', json=json_data)
        
        data_dict = resp.json().get("data")
        if data_dict is None:
            break
        row_diffs = data_dict.get("rowDiffs", dict())
        if row_diffs is None:
            break

        for rd in row_diffs.get("list", []):
            if len(rd.get("added")) == 0:
                continue

            yield rd.get("added").get("columnValues")[-1].get("displayValue")

        next_page_token = row_diffs.get("nextPageToken")

def main():
    json_data = {
        'operationName': 'PullsForRepo',
        'variables': {
            'ownerName': 'dolthub',
            'repoName': 'quest',
            'filterByState': 'Open',
        },
        'query': 'query PullsForRepo($ownerName: String!, $repoName: String!, $pageToken: String, $filterByState: PullState, $query: String) {\n  pulls(\n    ownerName: $ownerName\n    repoName: $repoName\n    pageToken: $pageToken\n    filterByState: $filterByState\n    query: $query\n  ) {\n    ...PullListForPullList\n    __typename\n  }\n}\n\nfragment PullListForPullList on PullList {\n  list {\n    ...PullForPullList\n    __typename\n  }\n  nextPageToken\n  __typename\n}\n\nfragment PullForPullList on Pull {\n  _id\n  createdAt\n  ownerName\n  repoName\n  pullId\n  creatorName\n  description\n  state\n  title\n  __typename\n}\n',
    }

    resp0 = requests.post('https://www.dolthub.com/graphql', json=json_data)
    
    seen_urls = dict()

    for d in reversed(resp0.json().get("data", dict()).get("pulls", dict()).get("list", [])):
        pull_id = d.get("pullId")
        
        for url in gen_mrf_urls(pull_id):
            if not url in seen_urls:
                print(url)
                seen_urls[url] = True

if __name__ == "__main__":
    main()

