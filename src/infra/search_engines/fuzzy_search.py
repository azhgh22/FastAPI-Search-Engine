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


    def fuzzy_intersection_with_fallback(self, query: str, max_results=10) -> List[int]:
        # Run both methods
        results_set = process.extract(
            query,
            self.search_choices,
            scorer=fuzz.token_set_ratio,
            limit=max_results * 3
        )

        results_partial = process.extract(
            query,
            self.search_choices,
            scorer=fuzz.partial_token_sort_ratio,
            limit=max_results * 3
        )

        # Convert to dict: id -> score
        set_dict = {match[2]: match[1] for match in results_set}
        partial_dict = {match[2]: match[1] for match in results_partial}

        # Intersection
        intersection_ids = set(set_dict.keys()) & set(partial_dict.keys())

        final_results = []

        for product_id in intersection_ids:
            final_results.append(product_id)

        if len(final_results) < max_results:
            for _, _, product_id in results_partial:
                if product_id not in final_results:
                    final_results.append(product_id)

                if len(final_results) >= max_results:
                    break

        return final_results[:max_results]


    def search(self, query: str, max_results: int = 10) -> List[Product]:
        if not query:
            return []

        query = query.lower()

        results = self.fuzzy_intersection_with_fallback(query, max_results)

        matched_products = []

        for product_id in results:
            product = self.db.get_product_by_id(product_id)
            if product:
                matched_products.append(product)

            

        return matched_products