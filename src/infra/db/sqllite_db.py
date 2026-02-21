import sqlite3
import json
from typing import List, Dict, Optional


class SqlLiteDB:
    def __init__(self, db_path: str = "products.db"):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                price REAL NOT NULL,
                country TEXT,
                brand TEXT,
                inStock BOOLEAN
            )
        ''')
        conn.commit()
        conn.close()

    def load_products_from_json(self, file_path: Optional[str] = None) -> List[Dict]:
        """Load products from a JSON file and return as list of dicts.

        Defaults to `src/infra/search_engines/products.json` when no path provided.
        """
        if file_path is None:
            file_path = "src/infra/search_engines/products.json"

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data

    def insert_products(self, products: List[Dict]):
        """Insert or replace a list of product dicts into the DB."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        stmt = (
            "INSERT OR REPLACE INTO products"
            "(id, name, description, price, country, brand, inStock)"
            "VALUES (?, ?, ?, ?, ?, ?, ?)"
        )

        rows = []
        for p in products:
            rows.append(
                (
                    p.get("id"),
                    p.get("name"),
                    p.get("description"),
                    p.get("price"),
                    p.get("country"),
                    p.get("brand"),
                    1 if p.get("inStock") else 0,
                )
            )

        cursor.executemany(stmt, rows)
        conn.commit()
        conn.close()

    def populate_from_json(self, file_path: Optional[str] = None):
        products = self.load_products_from_json(file_path)
        self.insert_products(products)