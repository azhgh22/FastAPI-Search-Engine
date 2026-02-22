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