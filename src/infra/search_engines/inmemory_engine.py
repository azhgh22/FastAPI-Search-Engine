from typing import List
from src.core.models.product import Product, ProductSearchRequest
from src.core.services.interfaces.file_readerI import FileReaderI

# implements SearchEngineI with an in-memory list of products for testing purposes
class InMemorySearchEngine:
    def __init__(self, file_reader: FileReaderI) -> None:
        pass

    def search(self, query: ProductSearchRequest, max_results: int = 10) -> List[Product]:
        return [Product(
            id=str(i),
            name=f"Product {i}",
            description=f"Description for product {i}",
            price=i * 10,
            brand="Brand X" if i % 3 == 0 else "Brand Y",
            country="Country 1" if i % 4 == 0 else "Country 2",
            inStock=True
        )    
        for i in range(max_results)]