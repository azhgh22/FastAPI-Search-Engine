from typing import Protocol
from enum import Enum

from src.core.services.interfaces.search_engineI import SearchEngineI

class EngineType(Enum):
    FUZZY = "fuzzy"
    VECTOR = "vector"

class EngineChooserI(Protocol):
    def choose_engine(self, engine_type: EngineType) -> SearchEngineI:
        """
        Given an engine type, return the appropriate engine identifier.
        Returns a string identifier for the chosen engine (e.g., "fuzzy", "vector").
        """
        pass