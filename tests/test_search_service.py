from src.core.services.interfaces.search_serviceI import SearchServiceI
from src.core.services.classes.search_service import SearchService
from src.core.models.product import Product, ProductSearchResponse
from src.core.models.product import ProductSearchRequest
import pytest

class MockSearchEngine:
    def search(self, query: ProductSearchRequest, max_results: int = 10):
        return [Product(
            id=str(i),
            name=f"Product {i}",
            description=f"Description for product {i}",
            price=10,
            brand="Brand X" if i % 3 == 0 else "Brand Y",
            country="Country 1" if i % 4 == 0 else "Country 2",
            inStock=True
        )    
        for i in range(max_results)]

class TestSearchService:
    @pytest.fixture
    def service(self) -> SearchServiceI:
        return SearchService(search_engine=MockSearchEngine())

    def test_search_price_should_be_formatted_correctly(self, service: SearchServiceI):
        query = ProductSearchRequest(name="Test", description="Test")
        results = service.search(query)
        assert all(isinstance(result, ProductSearchResponse) for result in results)
        assert results[0].name == "Product 0"
        assert results[0].description == "Description for product 0"
        assert results[0].price == "0.10"