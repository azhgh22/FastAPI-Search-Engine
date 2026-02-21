from typing import List
from fastapi import APIRouter
from pydantic import BaseModel
from src.core.models.product import Product, ProductSearchRequest
from src.core.services.interfaces.search_serviceI import SearchServiceI
from starlette.requests import Request

search_api = APIRouter()

def get_search_service(request: Request) -> SearchServiceI:
    return request.app.state.search_service

class SearchRequest(BaseModel):
    name: str
    description: str


@search_api.get("/", status_code=200)
def read_root():
    return {"message": "Hello, FastAPI!"}

@search_api.post("/", status_code=200)
def read_root(request: Request, search_request: SearchRequest) -> List[Product]:
    service_request = ProductSearchRequest(
                            name=search_request.name,
                            description=search_request.description
                        )
    search_service = get_search_service(request)
    return search_service.search(service_request)    