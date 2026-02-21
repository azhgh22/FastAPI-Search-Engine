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
    country: str
    brand: str
    price: str


@search_api.get("/", status_code=200)
def search():
    return {"message": "Hello, FastAPI!"}

@search_api.post("/vectorsearch", status_code=200)
def search_post(request: Request, search_request: SearchRequest) -> List[Product]:
    service_request = ProductSearchRequest(
                            name=search_request.name,
                            description=search_request.description,
                            country=search_request.country,
                            brand=search_request.brand,
                            price=search_request.price
                        )
    search_service = get_search_service(request)
    return search_service.search(service_request)


class FilterRequest(BaseModel):
    name: str
    country: str
    brand: str
    max_price: float
    min_price: float

@search_api.post("/filter", status_code=200)
def exact_match(request: Request, search_request: FilterRequest) -> List[Product]:
    search_service = get_search_service(request)
    return search_service.exact_filter(
        name=search_request.name,
        country=search_request.country,
        brand=search_request.brand,
        max_price=search_request.max_price,
        min_price=search_request.min_price
    )