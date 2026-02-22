

from src.core.services.interfaces.search_engineI import SearchEngineI


class HybridSearchEngine:
    def __init__(self, vector_engine:SearchEngineI, keyword_engine:SearchEngineI) -> None:
        self.vector_engine = vector_engine
        self.keyword_engine = keyword_engine

    def search(self, query: str, top_k=10):
        # Get results from both engines
        vector_results = self.vector_engine.search(query, top_k*3)
        keyword_results = self.keyword_engine.search(query, top_k*3)

        # get intersection of results
        vector_set = set(vector_results)
        keyword_set = set(keyword_results)

        intersection_product = vector_set & keyword_set

        # if intersection is too small, fill with keyword results
        if len(intersection_product) < top_k:
            only_in_keyword = keyword_set - vector_set

            for product in only_in_keyword:
                intersection_product.add(product)
                if len(intersection_product) >= top_k:
                    break


        return list(intersection_product)