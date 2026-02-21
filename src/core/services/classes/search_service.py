from typing import List

from src.core.models.product import Product, ProductSearchRequest
from src.core.services.interfaces.search_engineI import SearchEngineI


class SearchService:
    def __init__(self, search_engine: SearchEngineI):
        self.search_engine = search_engine
        
    def search(self, query: ProductSearchRequest) -> List[Product]:
        # handle messy inputes and convert them to a format that the search engine can understand
        # handle error cases and edge cases
        results = self.search_engine.search(query)
        # convert price from int to float string with 2 decimal places
        for result in results:
            result.price = f"{result.price // 100}.{result.price%100}"
        return results