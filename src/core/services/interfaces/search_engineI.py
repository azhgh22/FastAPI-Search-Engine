from typing import List, Protocol

from src.core.models.product import Product, ProductSearchRequest
from src.core.services.interfaces.products_dbI import ProductsDBI


class SearchEngineI(Protocol):
    def search(self, query: str, max_results: int = 10) -> List[Product]:
        pass

    def __call__(self, products_db: ProductsDBI) -> 'SearchEngineI':
        """
        Initialize the search engine with the given products database.
        This allows the search engine to access product data for searching.
        """
        pass