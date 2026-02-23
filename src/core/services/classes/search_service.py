from typing import List

from src.core.models.product import FuzzyProductRequest, Product, ProductSearchRequest
from src.core.services.interfaces.engine_chooserI import EngineChooserI, EngineType
from src.core.services.interfaces.products_dbI import ProductsDBI
from src.core.services.interfaces.search_engineI import SearchEngineI
from src.infra.db.inmem_db import InMemoryDB


class SearchService:
    def __init__(self, engine_chooser: EngineChooserI,db:ProductsDBI):
        self.engine_chooser = engine_chooser
        self.db = db

    def vector_search(self, query: ProductSearchRequest,count:int=10) -> List[Product]:
        # handle messy inputes and convert them to a format that the search engine can understand
        # handle error cases and edge cases
        query.description = query.description.lower().strip() if query.description else ""
        query.name = query.name.lower().strip() if query.name else ""

        query_fields = query.__dict__.keys()

        query_text = ""
        for field in query_fields:
            value:str = getattr(query, field)
            if value is not None and value != "":
                query_text += f"{field}: {value.lower().strip()}, "
        
        print(f"SearchService: Searching for query: {query_text}")

        engine = self.engine_chooser.choose_engine(EngineType.VECTOR)
        results = engine.search(query_text, count)
        return results
    
    def exact_filter(self, name: str, 
                     country: str, 
                     brand: str, 
                     max_price: float, 
                     min_price: float) -> List[Product]:
        

        return self.db.get_products_by_filter(name, country, brand, max_price, min_price,10)
    

    def fuzzy_search(self, query: FuzzyProductRequest,count:int = 10) -> List[Product]:
        name = (query.name or "").lower().strip()
        brand = (query.brand or "").lower().strip()
        description = (query.description or "").lower().strip()
        country = (query.country or "").lower().strip()

        query_text = f"{name} {brand} {description} {country}"

        engine = self.engine_chooser.choose_engine(EngineType.FUZZY)
        return engine.search(query_text,count)
    

    def hybrid_search(self, query: ProductSearchRequest,count:int = 10) -> List[Product]:
        name = (query.name or "").lower().strip()
        brand = (query.brand or "").lower().strip()
        description = (query.description or "").lower().strip()
        country = (query.country or "").lower().strip()

        fuzzy_query_text = f"{name} {brand} {description} {country}"

        vector_search_results = self.vector_search(query, count*3)
        
        db = InMemoryDB(products_path="", products=vector_search_results)
        fuzzy_engine = self.engine_chooser.choose_engine(EngineType.FUZZY)(db)
        fuzzy_results = fuzzy_engine.search(fuzzy_query_text, count)
        
        intersection_ids = set(p.id for p in vector_search_results) & set(p.id for p in fuzzy_results)
        print(f"SearchService: Intersection: {len(intersection_ids)}")
        
        return fuzzy_results
