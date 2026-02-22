from dataclasses import dataclass


@dataclass
class Product:
    id: int
    name: str
    description: str
    country: str
    brand: str
    inStock: bool
    price: float

    #define equality based on id only
    def __eq__(self, other):
        if isinstance(other, Product):
            return self.id == other.id
        return False
    
    def __hash__(self):
        return hash(self.id)


@dataclass
class ProductSearchRequest:
    name: str = ""
    description: str = ""
    country: str = ""
    brand: str = ""
    price: str = ""



@dataclass
class FuzzyProductRequest:
    name: str = ""
    description: str = ""
    country: str = ""
    brand: str = ""