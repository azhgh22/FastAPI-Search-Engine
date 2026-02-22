import os
import sqlite3
from typing import List, Dict, Optional
from src.core.models.product import Product
from src.infra.db.inmem_db import InMemoryDB


class SqlLiteDB:
    def __init__(self, db_path: str = "data_file/products.db"):
        self.db_path = db_path

        try:
            os.remove(db_path)
        except Exception as e:
            print(f"Error removing existing DB file: {e}")

        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._initialize_db()

    def _initialize_db(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                price REAL NOT NULL,
                country TEXT,
                brand TEXT,
                inStock INTEGER NOT NULL
            )
        ''')
        self.conn.commit()

        products = InMemoryDB(products_path="data_files/products.json").get_all_products()
        self.__insert_products(self.conn, products)

    def __insert_products(self, conn, products: List[Product]):
        """Insert or replace a list of product dicts into the DB."""

        stmt = (
            "INSERT OR REPLACE INTO products"
            "(id, name, description, price, country, brand, inStock)"
            "VALUES (?, ?, ?, ?, ?, ?, ?)"
        )

        cursor = conn.cursor()
        rows = []
        for p in products:
            rows.append(
                (
                    p.id,
                    p.name,
                    p.description,
                    p.price,
                    p.country,
                    p.brand,
                    1 if p.inStock else 0
                )
            )

        cursor.executemany(stmt, rows)
        conn.commit()

    def get_product_by_id(self, product_id: int) -> Product | None:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        row = cursor.fetchone()

        if row:
            return Product(
                id=row[0],
                name=row[1],
                description=row[2],
                price=row[3],
                country=row[4],
                brand=row[5],
                inStock=bool(row[6])
            )
        return None    

    def get_all_products(self) -> List[Product]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        products = []
        for row in rows:
            products.append(Product(
                id=row[0],
                name=row[1],
                description=row[2],
                price=row[3],
                country=row[4],
                brand=row[5],
                inStock=bool(row[6])
            ))
        return products
    
    def get_products_by_filter(self, name: str, 
                               country: str, 
                               brand: str, 
                               max_price: float, 
                               min_price: float,
                               max_samples: int) -> List[Product]:
        query = '''
            SELECT * FROM products 
            WHERE 1=1 and 
            (name LIKE ? and description LIKE ? and
            country LIKE ? and brand LIKE ? and price >= ? and price <= ?)
            LIMIT ?;

        '''

        cursor = self.conn.cursor()
        cursor.execute(query, (
            f"%{name}%" if name else "%",
            f"%{country}%" if country else "%",
            f"%{brand}%" if brand else "%",
            min_price if min_price is not None else 0,
            max_price if max_price is not None else float('inf'),
            max_samples if max_samples is not None else 1000,
        ))
        rows = cursor.fetchall()

        products: List[Product] = []
        for row in rows:
            products.append(Product(
                id=row[0],
                name=row[1],
                description=row[2],
                price=row[3],
                country=row[4],
                brand=row[5],
                inStock=bool(row[6])
            ))
        return products