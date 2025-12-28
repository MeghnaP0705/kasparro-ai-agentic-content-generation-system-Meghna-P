from models.product_model import ProductModel
from typing import Dict

class DataParserAgent:
    """Agent responsible for parsing and validating product data."""

    def __init__(self):
        self.agent_name = "DataParserAgent"
        self.input_schema = dict
        self.output_schema = ProductModel

    def execute(self, raw_data: Dict) -> ProductModel:
        """Parse raw data into ProductModel."""
        print(f"[{self.agent_name}] Parsing product data...")

        validated_data = self._validate_data(raw_data)
        product = ProductModel.from_dict(validated_data)

        print(f"[{self.agent_name}] Successfully parsed product: {product.name}")
        return product

    def _validate_data(self, data: Dict) -> Dict:
        """Validate required fields exist."""
        required_fields = ["name", "concentration", "skin_type", "key_ingredients", 
                          "benefits", "usage", "side_effects", "price"]

        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        return data
