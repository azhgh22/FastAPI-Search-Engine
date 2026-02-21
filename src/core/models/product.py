from dataclasses import dataclass


@dataclass
class Product:
    id: str
    name: str
    description: str
    country: str
    brand: str
    inStock: bool
    price: int


@dataclass
class ProductSearchRequest:
    name: str
    description: str

@dataclass
class ProductSearchResponse:
    id: str
    name: str
    description: str
    country: str
    brand: str
    inStock: bool
    price: str