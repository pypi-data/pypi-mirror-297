import logging
from typing import Union, List

from fastapi import APIRouter

from app.conf.basicConfig import search_manager
from app.conf.elasticConfig import DEFAULT_LIMIT
from app.conf.logConfig import LoggingRoute
from app.models import DetailedCriteria, IndexList, Criteria
from app.searchUtils import validate_indices

additional_router = APIRouter(tags=["Other Types of Search"], prefix="/search-service", route_class=LoggingRoute)
primary_router = APIRouter(tags=["Primary Search"], prefix="/search-service", route_class=LoggingRoute)

logger = logging.getLogger(__name__)


@primary_router.post("/document/op/getAll/")
async def search_documents_by_index(index_list: IndexList, limit: Union[int, None] = DEFAULT_LIMIT,
                                    with_grouping: Union[bool, None] = True):
    list_of_indices = validate_indices(index_list.indices)
    logger.info("Searching for all matches in index(/indices): " + str(list_of_indices))
    query_body = {"query": {"match_all": {}}}
    return search_manager.execute_query(list_of_indices, query_body, limit, with_grouping)


@primary_router.post("/document/op/searchForRecord")
async def search_by_specific_criteria(new_criteria: Criteria, limit: Union[int, None] = DEFAULT_LIMIT,
                                      with_grouping: Union[bool, None] = True):
    list_of_indices = validate_indices(new_criteria.index_list)
    conditions = [{"query_string": {"query": new_criteria.query.replace('"', '\\"'), "default_field": "*"}}]

    query_body = {"query": {"bool": {"must": conditions}}}
    logger.info("Searching in index(/indices): " + str(list_of_indices))
    logger.info("query Body: " + str(query_body))
    return search_manager.execute_query(list_of_indices, query_body, limit, with_grouping)


@additional_router.post("/document/op/searchWithExactMatch")
async def search_with_exact_match(criteria: DetailedCriteria, limit: Union[int, None] = DEFAULT_LIMIT,
                                  with_grouping: Union[bool, None] = True):
    list_of_indices = validate_indices(criteria.index_list)
    conditions = []
    for key, value in criteria.exact_match.items():
        conditions.append({"match": {key: value}})
    for key, value in criteria.query.items():
        conditions.append({"query_string": {"query": value, "default_field": key}})

    query_body = {"query": {"bool": {"must": conditions}}}
    logger.info(
        "Searching in the field(s): " + str(criteria.query.keys()) + " in index(/indices): " + str(list_of_indices))
    logger.info("query Body: " + str(query_body))
    return search_manager.execute_query(list_of_indices, query_body, limit, with_grouping)


@additional_router.get("/document/op/match")
async def search_match(index_list: IndexList, limit: Union[int, None] = DEFAULT_LIMIT, field: Union[str, None] = "",
                       query: Union[str, None] = "", operator: str = "or", with_grouping: Union[bool, None] = True):
    """Perform search by relevance for certain field and query."""
    list_of_indices = validate_indices(index_list.indices)
    logger.info(
        "Searching for " + query + " in the field(s): " + field + " in index(/indices): " + str(list_of_indices))
    query_body = {"query": {"match": {field: {"query": query, "operator": operator}}}}
    return search_manager.execute_query(list_of_indices, query_body, limit, with_grouping)


@additional_router.get("/document/op/wildcard")
async def search_wildcard(index_list: IndexList, limit: Union[int, None] = DEFAULT_LIMIT, field: Union[str, None] = "",
                          query: Union[str, None] = "", with_grouping: Union[bool, None] = True):
    list_of_indices = validate_indices(index_list.indices)
    logger.info(
        "Searching for " + query + " in the field(s): " + field + " in index(/indices): " + str(list_of_indices))
    query_body = {"query": {"wildcard": {field: query}}}
    return search_manager.execute_query(list_of_indices, query_body, limit, with_grouping)


@additional_router.post("/document/op/multiMatch")
async def search_multi_match(index_list: IndexList, limit: Union[int, None] = DEFAULT_LIMIT,
                             fields: Union[List[str], None] = None, query: Union[str, None] = "",
                             with_grouping: Union[bool, None] = True):
    """Perform search by relevance for certain field and query."""
    list_of_indices = validate_indices(index_list.indices)
    logger.info(
        "Searching for " + query + " in the field(s): " + str(fields) + " in index(/indices): " + str(list_of_indices))
    query_body = {"query": {"multi_match": {"query": query, "fields": fields}}}
    return search_manager.execute_query(list_of_indices, query_body, limit, with_grouping)


@additional_router.get("/document/op/search")
async def search_query_string(index_list: IndexList, limit: Union[int, None] = DEFAULT_LIMIT,
                              field: Union[str, None] = "", query: Union[str, None] = "",
                              with_grouping: Union[bool, None] = True):
    """Search by using operators with query string and size parameter"""
    list_of_indices = validate_indices(index_list.indices)
    logger.info("Searching for " + query + " in the field " + field + " in indices: " + str(list_of_indices))
    query_body = {"query": {"query_string": {"query": query, "default_field": field}}}
    return search_manager.execute_query(list_of_indices, query_body, limit, with_grouping)


@additional_router.get("/document/op/fuzzySearch")
async def search_fuzzy(index_list: IndexList, limit: Union[int, None] = DEFAULT_LIMIT,
                       field: Union[str, None] = "", query: Union[str, None] = "", fuzziness: Union[int, None] = 2,
                       with_grouping: Union[bool, None] = True):
    """Search by using fuzzy with query string and size parameter"""
    list_of_indices = validate_indices(index_list.indices)
    logger.info("Searching for " + query + " in the field " + field + " in indices: " + str(list_of_indices))
    query_body = {"query": {"fuzzy": {field: {"value": query, "fuzziness": fuzziness}}}}
    return search_manager.execute_query(list_of_indices, query_body, limit, with_grouping)


@additional_router.get("/document/op/searchByRange")
async def search_range(index_list: IndexList, limit: Union[int, None] = DEFAULT_LIMIT, field: Union[str, None] = "",
                       query: Union[str, None] = "", lte: Union[int, None] = 0, gte: Union[int, None] = 100,
                       with_grouping: Union[bool, None] = True):
    """Search by specifying a range of values for a field"""
    list_of_indices = validate_indices(index_list.indices)
    logger.info("Searching for " + query + " in the field " + field + " in indices: " + str(list_of_indices))
    query_body = {"query": {"range": {field: {"gte": gte, "lte": lte}}}}
    return search_manager.execute_query(list_of_indices, query_body, limit, with_grouping)


@additional_router.post("/document/op/searchByQuery")
async def search_by_query(index_list: IndexList, limit: Union[int, None] = DEFAULT_LIMIT,
                          query_body: Union[str, None] = "", with_grouping: Union[bool, None] = True):
    list_of_indices = validate_indices(index_list.indices)
    logger.info("Searching for " + query_body + " in index(/indices): " + str(list_of_indices))
    return search_manager.execute_query(list_of_indices, query_body, limit, with_grouping)
