from fastapi import FastAPI

from src.infra.API.search import search_api

def set_up_routes(api: FastAPI) -> None:
    api.include_router(search_api, prefix="/search", tags=["Search"])


def setup() -> FastAPI:
    api = FastAPI()
    set_up_routes(api)
    return api