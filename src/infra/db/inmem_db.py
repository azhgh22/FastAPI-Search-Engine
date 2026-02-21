import json
from typing import List, Dict
from src.core.models.product import Product

class InMemoryDB:
    def __init__(self, products_path:str):
        self.products_path = products_path
        self._initialize_db()

    def _initialize_db(self):
        product_dict = self.__load_products_from_json()
        self.products = self.__insert_products(product_dict)

    def __load_products_from_json(self) -> List[Dict]:
        with open(self.products_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data

    def __insert_products(self, products_dict: List[Dict]) -> dict[str, Product]:
        products: dict[str, Product] = {}

        for p in products_dict:
            products[p["id"]] = Product(
                id=p["id"],
                name=p["name"],
                description=p["description"],
                price=p["price"],
                country=p["country"],
                brand=p["brand"],
                inStock=p["inStock"]
            )

        return products

    def get_product_by_id(self, product_id: str) -> Product | None:
        return self.products.get(product_id)
        

    def get_all_products(self) -> List[Product]:
        return [p for p in self.products.values()]
    
    def get_products_by_filter(self, name: str, 
                               country: str, 
                               brand: str, 
                               max_price: float, 
                               min_price: float,
                               max_samples: int) -> List[Product]:
        filtered_products = []
        for product in self.products.values():
            if name and name != "" and name.lower() not in product.name.lower():
                continue
            if country and country != "" and country.lower() not in product.country.lower():
                continue
            if brand and brand != "" and brand.lower() not in product.brand.lower():
                continue
            if max_price is not None and product.price > max_price:
                continue
            if min_price is not None and product.price < min_price:
                continue
            filtered_products.append(product)
            if len(filtered_products) >= max_samples:
                break
        return filtered_products