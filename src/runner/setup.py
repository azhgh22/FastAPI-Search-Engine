from fastapi import FastAPI
from src.core.services.classes.search_service import SearchService
from src.core.services.interfaces.search_serviceI import SearchServiceI
from src.infra.API.search import search_api
from src.infra.db.inmem_db import InMemoryDB
from src.infra.search_engines.engine_chooser import EngineChooser
from src.infra.search_engines.fuzzy_search import FuzzySearchEngine
from src.infra.search_engines.vectorsearch_engine import VectorSearchEngine
from src.infra.db.sqllite_db import SqlLiteDB

def get_service() -> SearchServiceI:
    db = InMemoryDB(products_path="data_files/products.json")
    search_engine = VectorSearchEngine(products_db=db)
    engine_chooser = EngineChooser(fuzzy_engine=FuzzySearchEngine(db), vector_engine=search_engine)
    return SearchService(engine_chooser=engine_chooser, db=db)

def set_up_routes(api: FastAPI) -> None:
    api.include_router(search_api, prefix="/search", tags=["Search"])

def setup(search_service: SearchServiceI) -> FastAPI:
    api = FastAPI()
    set_up_routes(api)
    api.state.search_service = search_service
    return api