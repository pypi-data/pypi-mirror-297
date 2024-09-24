import logging

from fastapi import HTTPException

from app.models import SearchIndex

logger = logging.getLogger(__name__)


def validate_indices(indices: list, all_option=True):
    indices_set = set()
    for index in indices:
        if index.lower() in ["all", "*", "library.*"]:
            if not all_option:
                raise HTTPException(status_code=404, detail="Wrong Index: " + index)
            return ["library.*"]
        if index not in list(SearchIndex):
            raise HTTPException(status_code=404, detail="Wrong Index: " + index)

        indices_set.add(index)
    return list(indices_set)


def get_hits_as_result(es_resp, json_resp, with_grouping=True):
    if with_grouping:
        for hit in es_resp['hits']['hits']:
            if hit['_index'] not in json_resp.keys():
                json_resp[hit['_index']] = {"count": 1, "items": [hit['_source']]}
            else:
                json_resp[hit['_index']]['items'].append(hit['_source'])
                json_resp[hit['_index']]['count'] += 1
    else:
        if json_resp == {}:
            json_resp["all"] = {"count": 0, "items": []}
        for hit in es_resp['hits']['hits']:
            json_resp["all"]["count"] += 1
            json_resp["all"]["items"].append(hit['_source'])
            # json_resp["all"]["items"].append({"score": hit['_score'], "hit": hit['_source']})
