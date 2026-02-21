from typing import List, Protocol

from src.core.models.product import Product, ProductSearchRequest


class SearchEngineI(Protocol):
    def search(self, query: str, max_results: int = 10) -> List[Product]:
        pass