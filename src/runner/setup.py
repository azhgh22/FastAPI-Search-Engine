from fastapi import FastAPI
from src.core.services.classes.search_service import SearchService
from src.core.services.interfaces.search_serviceI import SearchServiceI
from src.infra.API.search import search_api
from src.infra.db.inmem_db import InMemoryDB
from src.infra.search_engines.vectorsearch_engine import VectorSearchEngine

def get_service_with_vector_engine() -> SearchServiceI:
    db = InMemoryDB(products_path="data_files/products.json")
    search_engine = VectorSearchEngine(products_db=db)
    return SearchService(search_engine=search_engine)

def set_up_routes(api: FastAPI) -> None:
    api.include_router(search_api, prefix="/search", tags=["Search"])

def setup(search_service: SearchServiceI) -> FastAPI:
    api = FastAPI()
    set_up_routes(api)
    api.state.search_service = search_service
    return api