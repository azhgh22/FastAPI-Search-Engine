from src.core.models.product import Product
from typing import List, Protocol

class ProductsDBI(Protocol):    
    def get_product_by_id(self, product_id: str) -> Product | None:
        pass

    def get_all_products(self) -> List[Product]:
        pass