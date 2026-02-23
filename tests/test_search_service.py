from src.core.services.interfaces.engine_chooserI import EngineType
from src.core.services.interfaces.products_dbI import ProductsDBI
from src.core.services.interfaces.search_engineI import SearchEngineI
from src.core.services.interfaces.search_serviceI import SearchServiceI
from src.core.services.classes.search_service import SearchService
from src.core.models.product import Product
from src.core.models.product import ProductSearchRequest
import pytest
from typing import Any, List

class MockSearchEngine:
    def search(self, query: str, max_results: int = 10) -> List[Product]:
        return [Product(
            id=i,
            name=f"Product {i}",
            description=f"Description for product {i}",
            price=10,
            brand="Brand X" if i % 3 == 0 else "Brand Y",
            country="Country 1" if i % 4 == 0 else "Country 2",
            inStock=True
        )    
        for i in range(max_results)]
    
    def __call__(self, products_db: ProductsDBI) -> SearchEngineI:
        """
        Initialize the search engine with the given products database.
        This allows the search engine to access product data for searching.
        """
        pass
    

class MockProductsDB:
    def get_product_by_id(self, product_id: int) -> Product | None:
        return None

    def get_all_products(self) -> List[Product]:
        return []

    def get_products_by_filter(self, name: str, 
                               country: str, 
                               brand: str, 
                               max_price: float, 
                               min_price: float,
                               max_samples: int) -> List[Product]:
        return [
            Product(
                id=0,
                name=f"Product {0}",
                description=f"Description for product {0}",
                price=10,
                brand="Brand X" if 0 % 3 == 0 else "Brand Y",
                country="Country 1" if 0 % 4 == 0 else "Country 2",
                inStock=True
            )
        ]

class MockEngineChooser:
    def choose_engine(self, engine_type: EngineType) -> SearchEngineI:
        return MockSearchEngine()

class TestSearchService:
    @pytest.fixture
    def service(self) -> SearchServiceI:
        engine_chooser = MockEngineChooser()        
        return SearchService(engine_chooser=engine_chooser, db=MockProductsDB())

    def test_search_price_should_be_formatted_correctly(self, service: SearchServiceI):
        query = ProductSearchRequest()
        results = service.vector_search(query)
        assert all(isinstance(result, Product) for result in results)
        assert results[0].name == "Product 0"
        assert results[0].description == "Description for product 0"
        assert results[0].price == 10


    def test_search_should_return_exact_match(self, service: SearchServiceI):
        results = service.exact_filter(name="product 0", country="", brand="", max_price=100, min_price=0)
        assert all(isinstance(result, Product) for result in results)
        assert len(results) == 1
        assert results[0].name == "Product 0"
        assert results[0].description == "Description for product 0"
        assert results[0].price == 10