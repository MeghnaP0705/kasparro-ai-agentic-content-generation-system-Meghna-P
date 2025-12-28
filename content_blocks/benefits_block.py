from models.product_model import ProductModel

class BenefitsBlock:
    """Generates benefits-related content."""

    def generate(self, product: ProductModel) -> dict:
        """Transform product benefits into structured content."""
        return {
            "benefits_list": product.benefits,
            "benefits_description": self._format_benefits(product),
            "key_benefit": product.benefits[0] if product.benefits else ""
        }

    def _format_benefits(self, product: ProductModel) -> str:
        """Format benefits into descriptive text."""
        if not product.benefits:
            return ""

        if len(product.benefits) == 1:
            return f"{product.name} provides {product.benefits[0].lower()} benefits."

        benefits_text = ", ".join(product.benefits[:-1]) + f" and {product.benefits[-1].lower()}"
        return f"{product.name} delivers {benefits_text} for your skin."
