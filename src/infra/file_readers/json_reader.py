import json
from pathlib import Path
from typing import List


class JsonReader:
    def __init__(self, file_path: str, max_items: int = 10000) -> None:
        self.file_path = Path(file_path)
        self.max_items = int(max_items)

    def read(self) -> List[dict]:
        if not self.file_path.exists():
            raise FileNotFoundError(f"JSON file not found: {self.file_path}")

        with self.file_path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)

        if not isinstance(data, list):
            raise ValueError("JSON root must be a list of product objects")

        results: List[dict] = []
        for item in data[: self.max_items]:
            if not isinstance(item, dict):
                continue
            normalized = dict(item)

            # ensure id is a string
            if "id" in normalized:
                normalized["id"] = str(normalized["id"])

            # normalize price to integer cents
            price = normalized.get("price", 0)
            try:
                price_float = float(price)
                price_cents = int(round(price_float * 100))
            except Exception:
                price_cents = 0
            normalized["price"] = price_cents

            results.append(normalized)

        return results