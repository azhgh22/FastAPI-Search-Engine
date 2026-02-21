from src.infra.file_readers.json_reader import JsonReader
import pytest
from typing import Any, List
import json

class TestJsonReader:
    @pytest.fixture
    def service(self): # -> tuple[List[dict], Any]:
        json_class = JsonReader(file_path="src/infra/search_engines/products.json", max_items=1)
        results = json_class.read()
        with json_class.file_path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        return results, data
        

    def test_reads_correctly(self, service: tuple[List[dict], Any]):
        results, data = service
        # print(data[0])
        assert all(isinstance(result, dict) for result in results)
        assert results[0]["name"] == data[0]["name"]
        assert results[0]["description"] == data[0]["description"]
        assert results[0]["price"]*1.0 == data[0]["price"] * 100