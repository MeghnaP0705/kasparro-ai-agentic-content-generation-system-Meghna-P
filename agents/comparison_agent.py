from agents.base_agent import BaseAgent
from messaging.message_types import Message, MessageType
from models.product_model import ProductModel
import random

class ComparisonAgent(BaseAgent):
    """Autonomous agent for product comparison."""

    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, message_bus)
        self.product_data = None

    def handle_message(self, message: Message):
        """Process messages autonomously."""

        if message.message_type == MessageType.INFORM:
            event = message.content.get("event")
            if event == "product_parsed":
                self.product_data = ProductModel.from_dict(message.content["product"])

        elif message.message_type == MessageType.REQUEST:
            action = message.content.get("action")

            if action == "generate_comparison":
                product_dict = message.content.get("product")

                if product_dict:
                    self.product_data = ProductModel.from_dict(product_dict)

                if not self.product_data:
                    self.send_message(
                        receiver=message.sender,
                        message_type=MessageType.ERROR,
                        content={"error": "Missing product data"},
                        conversation_id=message.conversation_id
                    )
                    return

                print(f"[{self.agent_id}] Creating fictional competitor product...")
                product_b = self._create_fictional_product(self.product_data)

                print(f"[{self.agent_id}] Generating comparison page...")
                comparison_page = self._generate_comparison(self.product_data, product_b)

                self.send_message(
                    receiver=message.sender,
                    message_type=MessageType.RESPONSE,
                    content={"comparison_page": comparison_page, "status": "success"},
                    conversation_id=message.conversation_id
                )

    def _create_fictional_product(self, base_product: ProductModel) -> ProductModel:
        """Generate fictional competitor product."""
        return ProductModel(
            name="RadiantGlow Vitamin C Essence",
            concentration="15% Vitamin C",
            skin_type=["Normal", "Dry"],
            key_ingredients=["Vitamin C", "Vitamin E", "Ferulic Acid"],
            benefits=["Anti-aging", "Brightening", "Hydration"],
            usage="Apply 3-4 drops in the evening after cleansing",
            side_effects="May cause slight irritation on very sensitive skin",
            price=random.choice([799, 899, 999])
        )

    def _generate_comparison(self, product_a: ProductModel, product_b: ProductModel) -> dict:
        """Generate comprehensive product comparison."""

        # Price comparison
        price_diff = product_a.price - product_b.price
        cheaper = product_a.name if price_diff < 0 else product_b.name

        # Ingredient comparison
        common_ingredients = list(set(product_a.key_ingredients) & set(product_b.key_ingredients))
        unique_a = list(set(product_a.key_ingredients) - set(product_b.key_ingredients))
        unique_b = list(set(product_b.key_ingredients) - set(product_a.key_ingredients))

        # Benefits comparison
        common_benefits = list(set(product_a.benefits) & set(product_b.benefits))
        unique_benefits_a = list(set(product_a.benefits) - set(product_b.benefits))
        unique_benefits_b = list(set(product_b.benefits) - set(product_a.benefits))

        # Skin type comparison
        common_skin = list(set(product_a.skin_type) & set(product_b.skin_type))
        unique_skin_a = list(set(product_a.skin_type) - set(product_b.skin_type))
        unique_skin_b = list(set(product_b.skin_type) - set(product_a.skin_type))

        # Winner determination
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
            "page_type": "Comparison",
            "comparison_title": f"{product_a.name} vs {product_b.name}",
            "products": {
                "product_a": {
                    "name": product_a.name,
                    "concentration": product_a.concentration,
                    "price": product_a.price,
                    "skin_type": product_a.skin_type,
                    "ingredients": product_a.key_ingredients,
                    "benefits": product_a.benefits,
                    "usage": product_a.usage
                },
                "product_b": {
                    "name": product_b.name,
                    "concentration": product_b.concentration,
                    "price": product_b.price,
                    "skin_type": product_b.skin_type,
                    "ingredients": product_b.key_ingredients,
                    "benefits": product_b.benefits,
                    "usage": product_b.usage
                }
            },
            "price_comparison": {
                "product_a_price": product_a.price,
                "product_b_price": product_b.price,
                "difference": abs(price_diff),
                "cheaper_product": cheaper,
                "percentage_difference": round((abs(price_diff) / max(product_a.price, product_b.price)) * 100, 2)
            },
            "ingredient_comparison": {
                "common_ingredients": common_ingredients,
                "unique_to_product_a": unique_a,
                "unique_to_product_b": unique_b,
                "total_ingredients_a": len(product_a.key_ingredients),
                "total_ingredients_b": len(product_b.key_ingredients)
            },
            "benefits_comparison": {
                "common_benefits": common_benefits,
                "unique_to_product_a": unique_benefits_a,
                "unique_to_product_b": unique_benefits_b
            },
            "skin_type_comparison": {
                "common_skin_types": common_skin,
                "unique_to_product_a": unique_skin_a,
                "unique_to_product_b": unique_skin_b
            },
            "winner_analysis": {
                "winner": winner,
                "score_product_a": score_a,
                "score_product_b": score_b,
                "reasoning": "Based on price, benefits count, and ingredients count"
            },
            "recommendation": f"Based on our analysis, {winner} offers better overall value." if winner != "Tie" else "Both products offer unique benefits. Choose based on your specific needs."
        }
