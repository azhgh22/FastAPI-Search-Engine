from src.core.models.product import Product
from src.core.services.interfaces.products_dbI import ProductsDBI
from src.infra.db.inmem_db import InMemoryDB
import pytest
from typing import Any
import json

class TestInMemoryDB:
    @pytest.fixture
    def service(self): # -> tuple[List[dict], Any]:
        with open("src/infra/search_engines/products.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return InMemoryDB(products_path="src/infra/search_engines/products.json"), data
        

    def test_reads_correctly(self, service: tuple[ProductsDBI, Any]):
        db, data = service

        first_id = data[0]["id"]

        from_db = db.get_product_by_id(first_id)
        assert from_db is not None
        assert from_db.name == data[0]["name"]
        assert from_db.description == data[0]["description"]
        assert from_db.price == data[0]["price"]

    def test_get_all_products(self, service: tuple[ProductsDBI, Any]):
        db, data = service

        all_products = db.get_all_products()
        assert len(all_products) == len(data)
        assert all(isinstance(p, Product) for p in all_products)