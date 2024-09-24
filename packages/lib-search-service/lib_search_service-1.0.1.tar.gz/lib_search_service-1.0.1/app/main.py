import logging

import uvicorn
from fastapi import FastAPI
from starlette.responses import RedirectResponse

from app.conf.basicConfig import SERVICE_URI, SERVICE_PORT
from app.routers import searchOperations, indexOperations

tags_metadata = [
    {
        "name": "Manipulation",
        "description": "Operations with Documents. This is a pre-configuration for our search service",
    },
    {
        "name": "Primary Search",
        "description": "The default search API to use",
    },
    {
        "name": "Other Types of Search",
        "description": "Search for Documents with Several Types.",
    },
    {
        "name": "Other Types of Informing",
        "description": "Different Types of Informing Elastic Search APIs."
    }
]

app = FastAPI(openapi_tags=tags_metadata, docs_url="/search-service/docs", openapi_url="/search-service/openapi.json")
app.include_router(searchOperations.primary_router)
app.include_router(indexOperations.primary_router)
# app.include_router(searchOperations.additional_router)
# app.include_router(indexOperations.additional_router)


@app.get("/search-service")
async def get_welcome_message():
    return {"message": "Welcome to our Search Service"}


@app.get("/search-service/openapi.json")
async def redirect_openapi():
    return RedirectResponse(url='/openapi.json')


if __name__ == '__main__':
    uvicorn.run('app.main:app', host=SERVICE_URI, port=SERVICE_PORT, reload=True, log_level=logging.DEBUG)
