from models.product_model import ProductModel

class ComparisonBlock:
    """Generates comparison content between products."""

    def compare_products(self, product_a: ProductModel, product_b: ProductModel) -> dict:
        """Compare two products across multiple dimensions."""
        return {
            "price_comparison": self._compare_prices(product_a, product_b),
            "ingredient_comparison": self._compare_ingredients(product_a, product_b),
            "benefits_comparison": self._compare_benefits(product_a, product_b),
            "skin_type_comparison": self._compare_skin_types(product_a, product_b),
            "winner_analysis": self._determine_winner(product_a, product_b)
        }

    def _compare_prices(self, product_a: ProductModel, product_b: ProductModel) -> dict:
        """Compare prices between products."""
        price_diff = product_a.price - product_b.price
        cheaper = product_a.name if price_diff < 0 else product_b.name

        return {
            "product_a_price": product_a.price,
            "product_b_price": product_b.price,
            "difference": abs(price_diff),
            "cheaper_product": cheaper,
            "percentage_difference": round((abs(price_diff) / max(product_a.price, product_b.price)) * 100, 2)
        }

    def _compare_ingredients(self, product_a: ProductModel, product_b: ProductModel) -> dict:
        """Compare ingredients between products."""
        common = list(set(product_a.key_ingredients) & set(product_b.key_ingredients))
        unique_a = list(set(product_a.key_ingredients) - set(product_b.key_ingredients))
        unique_b = list(set(product_b.key_ingredients) - set(product_a.key_ingredients))

        return {
            "common_ingredients": common,
            "unique_to_product_a": unique_a,
            "unique_to_product_b": unique_b,
            "total_ingredients_a": len(product_a.key_ingredients),
            "total_ingredients_b": len(product_b.key_ingredients)
        }

    def _compare_benefits(self, product_a: ProductModel, product_b: ProductModel) -> dict:
        """Compare benefits between products."""
        common = list(set(product_a.benefits) & set(product_b.benefits))
        unique_a = list(set(product_a.benefits) - set(product_b.benefits))
        unique_b = list(set(product_b.benefits) - set(product_a.benefits))

        return {
            "common_benefits": common,
            "unique_to_product_a": unique_a,
            "unique_to_product_b": unique_b
        }

    def _compare_skin_types(self, product_a: ProductModel, product_b: ProductModel) -> dict:
        """Compare skin type compatibility."""
        common = list(set(product_a.skin_type) & set(product_b.skin_type))
        unique_a = list(set(product_a.skin_type) - set(product_b.skin_type))
        unique_b = list(set(product_b.skin_type) - set(product_a.skin_type))

        return {
            "common_skin_types": common,
            "unique_to_product_a": unique_a,
            "unique_to_product_b": unique_b
        }

    def _determine_winner(self, product_a: ProductModel, product_b: ProductModel) -> dict:
        """Determine winner based on multiple factors."""
        score_a = 0
        score_b = 0

        if product_a.price < product_b.price:
            score_a += 1
        else:
            score_b += 1

        if len(product_a.benefits) > len(product_b.benefits):
            score_a += 1
        elif len(product_b.benefits) > len(product_a.benefits):
            score_b += 1

        if len(product_a.key_ingredients) > len(product_b.key_ingredients):
            score_a += 1
        elif len(product_b.key_ingredients) > len(product_a.key_ingredients):
            score_b += 1

        winner = product_a.name if score_a > score_b else product_b.name if score_b > score_a else "Tie"

        return {
            "winner": winner,
            "score_product_a": score_a,
            "score_product_b": score_b,
            "reasoning": f"Based on price, benefits count, and ingredients count"
        }
