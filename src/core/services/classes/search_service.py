from typing import List

from src.core.models.product import Product, ProductSearchRequest
from src.core.services.interfaces.search_engineI import SearchEngineI


class SearchService:
    def __init__(self, search_engine: SearchEngineI):
        self.search_engine = search_engine
        
    def search(self, query: ProductSearchRequest) -> List[Product]:
        # handle messy inputes and convert them to a format that the search engine can understand
        # handle error cases and edge cases
        query.description = query.description.lower().strip() if query.description else ""
        query.name = query.name.lower().strip() if query.name else ""

        query_fields = query.__dict__.keys()

        query_text = ""
        for field in query_fields:
            value:str = getattr(query, field)
            if value is not None and value != "":
                query_text += f"{field}: {value.lower().strip()}, "
        
        print(f"SearchService: Searching for query: {query_text}")


        results = self.search_engine.search(query_text)
        return results
    
