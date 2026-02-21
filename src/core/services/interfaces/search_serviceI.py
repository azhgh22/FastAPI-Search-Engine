from typing import List, Protocol

from src.core.models.product import ProductSearchRequest, ProductSearchResponse


class SearchServiceI(Protocol):
    def search(self, query: ProductSearchRequest) -> List[ProductSearchResponse]:
        pass