from models.product_model import ProductModel
from content_blocks.comparison_block import ComparisonBlock
import random

class ComparisonAgent:
    """Agent responsible for product comparison."""

    def __init__(self):
        self.agent_name = "ComparisonAgent"
        self.comparison_block = ComparisonBlock()

    def execute(self, product_a: ProductModel, product_b: ProductModel) -> dict:
        """Compare two products."""
        print(f"[{self.agent_name}] Comparing {product_a.name} vs {product_b.name}...")

        comparison_data = self.comparison_block.compare_products(product_a, product_b)

        print(f"[{self.agent_name}] Comparison complete")
        return comparison_data

    def create_fictional_product(self, base_product: ProductModel) -> ProductModel:
        """Generate fictional Product B with variations."""
        print(f"[{self.agent_name}] Creating fictional comparison product...")

        fictional_product = ProductModel(
            name="RadiantGlow Vitamin C Essence",
            concentration="15% Vitamin C",
            skin_type=["Normal", "Dry"],
            key_ingredients=["Vitamin C", "Vitamin E", "Ferulic Acid"],
            benefits=["Anti-aging", "Brightening", "Hydration"],
            usage="Apply 3-4 drops in the evening after cleansing",
            side_effects="May cause slight irritation on very sensitive skin",
            price=random.choice([799, 899, 999])
        )

        print(f"[{self.agent_name}] Created fictional product: {fictional_product.name}")
        return fictional_product
