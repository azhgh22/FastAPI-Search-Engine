from src.core.services.interfaces.engine_chooserI import EngineType
from src.core.services.interfaces.search_engineI import SearchEngineI
from src.infra.search_engines.vectorsearch_engine import VectorSearchEngine
from src.infra.search_engines.fuzzy_search import FuzzySearchEngine

class EngineChooser:
    def __init__(self, fuzzy_engine: FuzzySearchEngine, vector_engine: VectorSearchEngine):
        self.engine_dict = {
            EngineType.FUZZY: fuzzy_engine,
            EngineType.VECTOR: vector_engine
        }

    def choose_engine(self, engine_type: EngineType) -> SearchEngineI:
        """
        Given an engine type, return the appropriate engine identifier.
        Returns a string identifier for the chosen engine (e.g., "fuzzy", "vector").
        """
        return self.engine_dict[engine_type]