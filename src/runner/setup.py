from fastapi import FastAPI
from dataclasses import dataclass
from src.core.services.classes.search_service import SearchService
from src.core.services.interfaces.search_engineI import SearchEngineI
from src.core.services.interfaces.search_serviceI import SearchServiceI
from src.infra.API.search import search_api
from src.infra.file_readers.json_reader import JsonReader
from src.infra.search_engines.inmemory_engine import InMemorySearchEngine

def get_service_with_in_mem_engine() -> SearchServiceI:
    search_engine = InMemorySearchEngine(JsonReader(file_path="src/infra/search_engines/products.json"))
    return SearchService(search_engine=search_engine)

def set_up_routes(api: FastAPI) -> None:
    api.include_router(search_api, prefix="/search", tags=["Search"])

def setup(search_service: SearchServiceI) -> FastAPI:
    api = FastAPI()
    set_up_routes(api)
    api.state.search_service = search_service
    return api