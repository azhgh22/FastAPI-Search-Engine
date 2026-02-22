from typing import List
from src.core.models.product import Product, ProductSearchRequest
from src.core.services.interfaces.products_dbI import ProductsDBI
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import os



# implements SearchEngineI with an in-memory list of products for testing purposes
class VectorSearchEngine:
    def __init__(self, products_db: ProductsDBI) -> None:
        self.db = products_db

        self.index_path = "data_files/vector_search_all_MiniLM_L6_v2/products.index"
        self.id_map_path = "data_files/vector_search_all_MiniLM_L6_v2/id_map.json"

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        if os.path.exists(self.index_path) and os.path.exists(self.id_map_path):
            try:
                self.index = faiss.read_index(self.index_path)

                with open(self.id_map_path, "r") as f:
                    self.id_map = json.load(f)

                print("Loaded existing vector index.")
                return
            except Exception as e:
                print(f"Failed to load existing index: {e}")
                print("Rebuilding index...")

        self.__load_and_build_index()

    def _build_search_text(self, p: Product) -> str:
        """
        Create weighted searchable representation.
        Name and brand are prioritized.
        """
        name = (p.name or "").lower().strip()
        brand = (p.brand or "").lower().strip()
        description = (p.description or "").lower().strip()
        country = (p.country or "").lower().strip()
        price = str(p.price).lower() if p.price is not None else ""
        in_stock = "yes" if p.inStock else "no"


        return str({
            "name": name,
            "brand": brand,
            "name": name,
            "brand": brand,
            "description": description,
            "country": country,
            "country": country,
            "price": price,
            "price": price,
            "price": price,
            "in_stock": in_stock
        })

        # Name and brand appear twice to increase importance
        # return f"{name} {name} {brand} {brand} {description} {country} {price} {price} {price} {in_stock}"

    def __load_and_build_index(self):
        products = self.db.get_all_products()

        if not products:
            print("No products found in DB.")
            self.index = None
            self.id_map = []
            return

        texts = [self._build_search_text(p) for p in products]

        # Generate embeddings
        embeddings = self.model.encode(texts, show_progress_bar=True)
        embeddings = np.array(embeddings).astype("float32")

        # Normalize for cosine similarity
        faiss.normalize_L2(embeddings)

        dimension = embeddings.shape[1]
        index = faiss.IndexFlatIP(dimension)

        # Add vectors (correct FAISS usage)
        index.add(embeddings) # type: ignore

        # Save index
        faiss.write_index(index, self.index_path)

        # Save ID mapping (index → product_id)
        self.id_map = [p.id for p in products]
        with open(self.id_map_path, "w") as f:
            json.dump(self.id_map, f)

        self.index = index

        print("Vector index built successfully.")

    def search(self, query: str, max_results: int = 10) -> List[Product]:
        if not self.index:
            return []

        # Combine name + description into one search text
        search_text = query.strip()

        if not search_text:
            return []

        # Encode query
        query_embedding = self.model.encode([search_text])
        query_embedding = np.array(query_embedding).astype("float32")

        # Normalize for cosine similarity
        faiss.normalize_L2(query_embedding)

        # Search
        distances, indices = self.index.search(query_embedding, max_results) # type: ignore

        results: List[Product] = []

        for idx in indices[0]:
            if idx == -1:
                continue

            product_id = self.id_map[idx]
            product = self.db.get_product_by_id(product_id)

            if product:
                results.append(product)

        return results