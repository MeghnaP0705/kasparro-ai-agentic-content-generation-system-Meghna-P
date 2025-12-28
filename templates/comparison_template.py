from templates.base_template import BaseTemplate
from models.product_model import ProductModel
from typing import Dict

class ComparisonTemplate(BaseTemplate):
    """Template for comparison page generation."""

    def define_structure(self):
        """Define comparison template structure."""
        self.fields = ["product_a", "product_b", "comparison_data"]
        self.rules = {
            "comparison_dimensions": ["price", "ingredients", "benefits", "skin_type"]
        }

    def render(self, product_a: ProductModel, product_b: ProductModel, comparison_data: dict) -> dict:
        """Render comparison page."""
        return {
            "page_type": "Comparison",
            "comparison_title": f"{product_a.name} vs {product_b.name}",
            "products": {
                "product_a": self._format_product(product_a),
                "product_b": self._format_product(product_b)
            },
            "price_comparison": comparison_data.get("price_comparison", {}),
            "ingredient_comparison": comparison_data.get("ingredient_comparison", {}),
            "benefits_comparison": comparison_data.get("benefits_comparison", {}),
            "skin_type_comparison": comparison_data.get("skin_type_comparison", {}),
            "winner_analysis": comparison_data.get("winner_analysis", {}),
            "recommendation": self._create_recommendation(comparison_data)
        }

    def _format_product(self, product: ProductModel) -> dict:
        """Format product data for comparison."""
        return {
            "name": product.name,
            "concentration": product.concentration,
            "price": product.price,
            "skin_type": product.skin_type,
            "ingredients": product.key_ingredients,
            "benefits": product.benefits,
            "usage": product.usage
        }

    def _create_recommendation(self, comparison_data: dict) -> str:
        """Create recommendation based on comparison."""
        winner_data = comparison_data.get("winner_analysis", {})
        winner = winner_data.get("winner", "")

        if winner and winner != "Tie":
            return f"Based on our analysis, {winner} offers better overall value."

        return "Both products offer unique benefits. Choose based on your specific needs."
