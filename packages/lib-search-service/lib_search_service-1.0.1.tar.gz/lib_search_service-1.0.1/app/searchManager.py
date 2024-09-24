import logging

from elasticsearch import Elasticsearch
from fastapi import HTTPException

from app.conf.elasticConfig import ELASTIC_SEARCH_SERVICE_URI, ELASTIC_PASSWORD
from app.models import SearchIndex
from app.searchUtils import get_hits_as_result

logger = logging.getLogger(__name__)


class SearchManager:
    def __init__(self):

        logger.info("Initializing Search Manager..")

        # Create the client instance
        self.client = Elasticsearch(
            ELASTIC_SEARCH_SERVICE_URI,
            verify_certs=False,
            basic_auth=("elastic", ELASTIC_PASSWORD)
        )

        if not self.client.ping:
            raise ValueError("Connection failed")

        logger.info("Adding Default Indices to our Elastic Search..")
        for default_index in list(SearchIndex):
            if not self.client.indices.exists(index=default_index):
                self.client.indices.create(index=default_index)
                logger.info("index: " + default_index + " Has Been Added Successfully")
            else:
                logger.info("index: " + default_index + " is duplicated")

        logger.info("Elastic Search Client Connected Successfully")

    def execute_query(self, list_of_indices, query_body, limit, with_grouping):
        json_resp = {}
        try:
            es_resp = self.client.search(index=list_of_indices, body=query_body, size=limit)
            # logger.info("response for search: " + str(es_resp))
        except ConnectionError as err:
            raise HTTPException(status_code=404, detail="Cannot connect to elastic, " + str(err))
        except Exception as err:
            raise HTTPException(status_code=404, detail=err)
        logger.info("For index(or indices): %s, Got %d Hits" % (list_of_indices, es_resp['hits']['total']['value']))
        get_hits_as_result(es_resp, json_resp, with_grouping)
        return json_resp
