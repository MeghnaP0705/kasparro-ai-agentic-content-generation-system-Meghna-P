from dataclasses import dataclass, field
from typing import List

@dataclass
class ProductModel:
    """Clean internal representation of product data."""
    name: str
    concentration: str
    skin_type: List[str]
    key_ingredients: List[str]
    benefits: List[str]
    usage: str
    side_effects: str
    price: int

    @classmethod
    def from_dict(cls, data: dict):
        """Create ProductModel from dictionary."""
        return cls(
            name=data["name"],
            concentration=data["concentration"],
            skin_type=data["skin_type"],
            key_ingredients=data["key_ingredients"],
            benefits=data["benefits"],
            usage=data["usage"],
            side_effects=data["side_effects"],
            price=data["price"]
        )

    def to_dict(self) -> dict:
        """Convert ProductModel to dictionary."""
        return {
            "name": self.name,
            "concentration": self.concentration,
            "skin_type": self.skin_type,
            "key_ingredients": self.key_ingredients,
            "benefits": self.benefits,
            "usage": self.usage,
            "side_effects": self.side_effects,
            "price": self.price
        }
