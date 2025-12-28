from templates.base_template import BaseTemplate
from models.product_model import ProductModel
from typing import Dict

class ProductPageTemplate(BaseTemplate):
    """Template for product page generation."""

    def define_structure(self):
        """Define product page template structure."""
        self.fields = ["name", "description", "benefits", "usage", "ingredients", "pricing"]
        self.rules = {
            "required_sections": ["overview", "benefits", "usage", "ingredients", "details"]
        }

    def render(self, content_data: dict, product: ProductModel) -> dict:
        """Render complete product page."""
        return {
            "page_type": "Product Page",
            "product_name": product.name,
            "overview": self._create_overview(product),
            "benefits": self._create_benefits_section(content_data, product),
            "ingredients": self._create_ingredients_section(content_data, product),
            "usage": self._create_usage_section(content_data, product),
            "details": self._create_details_section(product),
            "pricing": {
                "price": product.price,
                "currency": "INR",
                "formatted_price": f"₹{product.price}"
            }
        }

    def _create_overview(self, product: ProductModel) -> dict:
        """Create product overview section."""
        return {
            "title": product.name,
            "subtitle": product.concentration,
            "description": f"A premium skincare serum designed for {' and '.join(product.skin_type).lower()} skin types."
        }

    def _create_benefits_section(self, content_data: dict, product: ProductModel) -> dict:
        """Create benefits section."""
        benefits_content = content_data.get("benefits", {})
        return {
            "heading": "Key Benefits",
            "description": benefits_content.get("benefits_description", ""),
            "benefits_list": benefits_content.get("benefits_list", product.benefits)
        }

    def _create_ingredients_section(self, content_data: dict, product: ProductModel) -> dict:
        """Create ingredients section."""
        ingredients_content = content_data.get("ingredients", {})
        return {
            "heading": "Key Ingredients",
            "description": ingredients_content.get("ingredients_description", ""),
            "ingredients_list": ingredients_content.get("ingredients_list", product.key_ingredients),
            "primary_ingredient": ingredients_content.get("primary_ingredient", "")
        }

    def _create_usage_section(self, content_data: dict, product: ProductModel) -> dict:
        """Create usage section."""
        usage_content = content_data.get("usage", {})
        return {
            "heading": "How to Use",
            "instructions": usage_content.get("instructions", product.usage),
            "frequency": usage_content.get("frequency", ""),
            "timing": usage_content.get("timing", ""),
            "application_method": usage_content.get("application_method", "")
        }

    def _create_details_section(self, product: ProductModel) -> dict:
        """Create product details section."""
        return {
            "skin_type": product.skin_type,
            "concentration": product.concentration,
            "side_effects": product.side_effects,
            "safety_note": f"Note: {product.side_effects}"
        }
