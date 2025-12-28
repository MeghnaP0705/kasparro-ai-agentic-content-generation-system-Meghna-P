from models.product_model import ProductModel

class IngredientsBlock:
    """Generates ingredient-related content."""

    def generate(self, product: ProductModel) -> dict:
        """Transform ingredients into structured content."""
        return {
            "ingredients_list": product.key_ingredients,
            "ingredients_description": self._format_ingredients(product),
            "primary_ingredient": product.key_ingredients[0] if product.key_ingredients else ""
        }

    def _format_ingredients(self, product: ProductModel) -> str:
        """Format ingredients into descriptive text."""
        if not product.key_ingredients:
            return ""

        if len(product.key_ingredients) == 1:
            return f"Formulated with {product.key_ingredients[0]}."

        ingredients_text = ", ".join(product.key_ingredients[:-1]) + f" and {product.key_ingredients[-1]}"
        return f"Key ingredients include {ingredients_text}."
