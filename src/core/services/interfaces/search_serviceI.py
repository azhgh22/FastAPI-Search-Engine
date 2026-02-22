from typing import List, Protocol

from src.core.models.product import Product, ProductSearchRequest, FuzzyProductRequest


class SearchServiceI(Protocol):
    def search(self, query: ProductSearchRequest) -> List[Product]:
        pass

    def exact_filter(self, name: str, 
                     country: str, 
                     brand: str, 
                     max_price: float, 
                     min_price: float) -> List[Product]:
        pass

    def fuzzy_search(self, query: FuzzyProductRequest) -> List[Product]:
        pass