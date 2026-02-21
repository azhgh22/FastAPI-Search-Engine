from src.core.models.product import Product
from src.core.services.interfaces.products_dbI import ProductsDBI
from src.infra.db.inmem_db import InMemoryDB
import pytest

from src.infra.search_engines.vectorsearch_engine import VectorSearchEngine

class TestVectorSearchEngine:
    @pytest.fixture
    def engine(self): # -> tuple[List[dict], Any]:
        db = InMemoryDB(products_path="src/infra/search_engines/products.json")
        return VectorSearchEngine(products_db=db)

    def test_env_works(self, engine: VectorSearchEngine) -> None:
        assert True