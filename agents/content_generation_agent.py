from models.product_model import ProductModel
from typing import List, Dict

class ContentGenerationAgent:
    """Agent responsible for generating structured content using blocks and templates."""

    def __init__(self, content_blocks: List, template):
        self.agent_name = "ContentGenerationAgent"
        self.content_blocks = content_blocks
        self.template = template

    def execute(self, product: ProductModel, additional_data: Dict = None) -> dict:
        """Generate content by applying content blocks and rendering template."""
        print(f"[{self.agent_name}] Generating content for {product.name}...")

        content_parts = {}
        for block in self.content_blocks:
            block_name = block.__class__.__name__.replace("Block", "").lower()
            content_parts[block_name] = block.generate(product)

        if additional_data:
            output = self.template.render(additional_data, product)
        else:
            output = self.template.render(content_parts, product)

        print(f"[{self.agent_name}] Content generation complete")
        return output
