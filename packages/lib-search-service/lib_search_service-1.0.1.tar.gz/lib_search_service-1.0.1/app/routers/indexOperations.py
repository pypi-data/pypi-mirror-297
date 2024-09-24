import json
import logging
from typing import Union, List, Dict

import elasticsearch
from elasticsearch import helpers
from fastapi import HTTPException, APIRouter

from app.conf.basicConfig import search_manager
from app.conf.logConfig import LoggingRoute
from app.models import Folder, Course, Faculty, Major, SearchIndex, IndexList
from app.searchUtils import validate_indices

primary_router = APIRouter(tags=["Search Informer"], prefix="/search-service", route_class=LoggingRoute)
additional_router = APIRouter(tags=["Other Types of Informing"], prefix="/search-service", route_class=LoggingRoute)

logger = logging.getLogger(__name__)


@primary_router.post("/folder/op/add")
async def add_search_info(folder: Folder):
    folder.type = SearchIndex.FOLDER
    search_manager.client.index(index=folder.type, id=folder.id, document=json.dumps(folder.__dict__))
    logger.info("folder with ID %s has been added successfully" % folder.id)
    return "Done"


@primary_router.post("/course/op/add")
async def add_search_info(course: Course):
    course.type = SearchIndex.COURSE
    search_manager.client.index(index=course.type, id=course.id, document=json.dumps(course.__dict__))
    logger.info("course with ID %s has been added successfully" % course.id)
    return "Done"


@primary_router.post("/major/op/add")
async def add_search_info(major: Major):
    major.type = SearchIndex.MAJOR
    search_manager.client.index(index=major.type, id=major.id, document=json.dumps(major.__dict__))
    logger.info("major with ID %s has been added successfully" % major.id)
    return "Done"


@primary_router.post("/faculty/op/add")
async def add_search_info(faculty: Faculty):
    faculty.type = SearchIndex.FACULTY
    search_manager.client.index(index=faculty.type, id=faculty.id, document=json.dumps(faculty.__dict__))
    logger.info("faculty with ID %s has been added successfully" % faculty.id)
    return "Done"


@primary_router.delete("/document/op/delete")
async def delete_document(id: str = None, type: str = None):
    if id is None:
        raise HTTPException(status_code=404, detail="Missing required parameter: id")
    if type is None:
        raise HTTPException(status_code=404, detail="Missing required parameter: type")
    try:
        list_of_indices = validate_indices([type], all_option=False)
        for index in list_of_indices:
            logger.info("index: " + index)
            if search_manager.client.exists(index=index, id=id):
                search_manager.client.delete(index=index, id=id)
                logger.info("Document with ID %s in index %s has been deleted successfully" % (id, index))
    except elasticsearch.NotFoundError:
        raise HTTPException(status_code=404, detail="Cannot Find this document!")

    return "Done"


@additional_router.post("/document/op/add")
async def add_document(document: Dict[str, str]):
    index_name = validate_indices([document.get("type")], all_option=False)
    search_manager.client.index(index=index_name, id=document.get("id"), document=document)
    logger.info("Document with ID %s in index %s has been added successfully" % (document.get("id"), index_name))
    return "Done"


@additional_router.post("/documents/op/add")
async def add_documents(document_list: List[Dict[str, str]]):
    document_list = prepare_documents_to_bulk(document_list)
    response = helpers.bulk(search_manager.client, document_list)
    logger.info(f"Data sent to your ElasticSearch with response: {response}")
    return "Done"


@additional_router.delete("/index/op/delete")
async def delete_index(index_name: Union[str, None] = None):
    if not search_manager.client.indices.exists(index=index_name):
        return "Index " + index_name + " Does not exist"
    es_resp = search_manager.client.indices.delete(index=index_name)
    return es_resp


@additional_router.delete("/document/op/deleteWithBody")
async def delete_documents(index_name: IndexList, document_id: Union[str, None] = None):
    list_of_indices = validate_indices(index_name.indices, all_option=False)
    if document_id is None:
        try:
            search_manager.client.delete_by_query(index=list_of_indices, body={"query": {"match_all": {}}})
            logger.info("Documents in index %s has been deleted successfully" % list_of_indices)
        except Exception:
            raise HTTPException(status_code=404, detail="Failed to delete with index: " + str(list_of_indices))
    else:
        try:
            for index in list_of_indices:
                logger.info("index: " + index)
                if search_manager.client.exists(index=index, id=document_id):
                    search_manager.client.delete(index=index, id=document_id)
                    logger.info("Document with ID %s in index %s has been deleted successfully" % (
                        document_id, index))
        except elasticsearch.NotFoundError:
            raise HTTPException(status_code=404, detail="Cannot Find this document!")

    return "Done"


@additional_router.put("/documents/op/load")
async def load_documents():
    def read_data():
        """Yields json_data from json file."""
        # Test Source
        with open("../conf/initialData/full_format_documents.json", "r") as f:
            json_data = json.load(f)
            logger.info(json.dumps(json_data, indent=2))
            return prepare_documents_to_bulk(json_data)

    data = read_data()
    response = helpers.bulk(search_manager.client, data)
    logger.info(f"Data sent to your ElasticSearch with response: {response}")
    return "Done"


def prepare_documents_to_bulk(document_list):
    # Need to validate every type here
    actions = [
        {
            "_index": document['type'],
            "_id": document['id'],
            "_source": document
        } for document in document_list
    ]
    return actions
