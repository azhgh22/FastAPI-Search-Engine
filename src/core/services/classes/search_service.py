from typing import List

from src.core.models.product import ProductSearchRequest, ProductSearchResponse
from src.core.services.interfaces.search_engineI import SearchEngineI


class SearchService:
    def __init__(self, search_engine: SearchEngineI):
        self.search_engine = search_engine
        
    def search(self, query: ProductSearchRequest) -> List[ProductSearchResponse]:
        # handle messy inputes and convert them to a format that the search engine can understand
        # handle error cases and edge cases
        results = self.search_engine.search(query)
        # convert price from int to float string with 2 decimal places
        results = [ProductSearchResponse(
                        id=result.id,
                        name=result.name,
                        description=result.description,
                        price=f"{result.price // 100}.{result.price % 100}",
                        brand=result.brand,
                        country=result.country,
                        inStock=result.inStock
                        ) for result in results]
        return results