from src.core.models.product import Product
from typing import List, Protocol

class ProductsDBI(Protocol):    
    def get_product_by_id(self, product_id: str) -> Product | None:
        pass

    def get_all_products(self) -> List[Product]:
        pass

    def get_products_by_filter(self, name: str, 
                               country: str, 
                               brand: str, 
                               max_price: float, 
                               min_price: float,
                               max_samples: int) -> List[Product]:
        pass