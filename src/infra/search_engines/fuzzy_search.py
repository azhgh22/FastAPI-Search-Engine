from typing import List
from rapidfuzz import fuzz, process
from src.core.services.interfaces.products_dbI import ProductsDBI
from src.core.models.product import Product


class FuzzySearchEngine:
    def __init__(self, products_db: ProductsDBI) -> None:
        self.db = products_db
        self.products: List[Product] = self.db.get_all_products()

        # Build searchable text per product
        # We combine important text fields
        self.search_choices = {
            p.id: self._build_search_text(p)
            for p in self.products
        }

    def _build_search_text(self, p: Product) -> str:
        """
        Create weighted searchable representation.
        Name and brand are prioritized.
        """
        name = (p.name or "").lower().strip()
        brand = (p.brand or "").lower().strip()
        description = (p.description or "").lower().strip()
        country = (p.country or "").lower().strip()

        # Name and brand appear twice to increase importance
        return f"{name} {name} {brand} {brand} {description} {country}"

    def search(self, query: str, max_results: int = 10) -> List[Product]:
        if not query:
            return []

        query = query.lower()

        results = process.extract(
            query,
            self.search_choices,
            scorer=fuzz.token_set_ratio,
            limit=max_results,  # get more candidates
        )

        matched_products = []

        for _, score, product_id in results:
            if score >= 60:  # threshold (tune this)
                product = self.db.get_product_by_id(product_id)
                if product:
                    matched_products.append(product)

            if len(matched_products) >= max_results:
                break

        return matched_products