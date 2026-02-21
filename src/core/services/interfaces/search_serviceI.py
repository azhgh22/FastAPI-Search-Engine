from typing import List, Protocol

from src.core.models.product import Product, ProductSearchRequest


class SearchServiceI(Protocol):
    def search(self, query: ProductSearchRequest) -> List[Product]:
        pass