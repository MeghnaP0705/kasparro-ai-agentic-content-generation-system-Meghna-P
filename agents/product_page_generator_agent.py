from agents.base_agent import BaseAgent
from messaging.message_types import Message, MessageType
from models.product_model import ProductModel

class ProductPageGeneratorAgent(BaseAgent):
    """Autonomous agent for generating product pages."""

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

            if action == "generate_product_page":
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

                print(f"[{self.agent_id}] Generating product page...")
                product_page = self._generate_product_page(self.product_data)

                self.send_message(
                    receiver=message.sender,
                    message_type=MessageType.RESPONSE,
                    content={"product_page": product_page, "status": "success"},
                    conversation_id=message.conversation_id
                )

    def _generate_product_page(self, product: ProductModel) -> dict:
        """Generate complete product page."""
        return {
            "page_type": "Product Page",
            "product_name": product.name,
            "overview": {
                "title": product.name,
                "subtitle": product.concentration,
                "description": f"A premium skincare serum designed for {' and '.join(product.skin_type).lower()} skin types."
            },
            "benefits": {
                "heading": "Key Benefits",
                "description": f"{product.name} delivers {' and '.join([b.lower() for b in product.benefits])} for your skin.",
                "benefits_list": product.benefits
            },
            "ingredients": {
                "heading": "Key Ingredients",
                "description": f"Formulated with {', '.join(product.key_ingredients[:-1])} and {product.key_ingredients[-1]}.",
                "ingredients_list": product.key_ingredients,
                "primary_ingredient": product.key_ingredients[0]
            },
            "usage": {
                "heading": "How to Use",
                "instructions": product.usage,
                "frequency": "Once daily",
                "timing": "Morning",
                "application_method": "2-3 drops"
            },
            "details": {
                "skin_type": product.skin_type,
                "concentration": product.concentration,
                "side_effects": product.side_effects,
                "safety_note": f"Note: {product.side_effects}"
            },
            "pricing": {
                "price": product.price,
                "currency": "INR",
                "formatted_price": f"₹{product.price}"
            }
        }
