from agents.base_agent import BaseAgent
from messaging.message_types import Message, MessageType
from models.product_model import ProductModel

class FAQGeneratorAgent(BaseAgent):
    """Autonomous agent for generating FAQ pages."""

    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, message_bus)
        self.product_data = None
        self.questions = None

    def handle_message(self, message: Message):
        """Process messages autonomously."""

        # Listen for broadcasts
        if message.message_type == MessageType.INFORM:
            event = message.content.get("event")
            if event == "product_parsed":
                self.product_data = ProductModel.from_dict(message.content["product"])

        # Handle requests
        elif message.message_type == MessageType.REQUEST:
            action = message.content.get("action")

            if action == "generate_faq":
                product_dict = message.content.get("product")
                questions = message.content.get("questions")

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

                print(f"[{self.agent_id}] Generating FAQ page...")
                faq_page = self._generate_faq_page(questions, self.product_data)

                # Send response
                self.send_message(
                    receiver=message.sender,
                    message_type=MessageType.RESPONSE,
                    content={"faq_page": faq_page, "status": "success"},
                    conversation_id=message.conversation_id
                )

    def _generate_faq_page(self, questions: list, product: ProductModel) -> dict:
        """Generate FAQ page with answers."""
        faqs = []

        for q in questions[:15]:  # Minimum 15 questions
            faq_item = {
                "question": q["question"],
                "answer": self._generate_answer(q, product),
                "category": q["category"]
            }
            faqs.append(faq_item)

        return {
            "page_type": "FAQ",
            "product_name": product.name,
            "total_questions": len(faqs),
            "faqs": faqs,
            "categories": list(set([faq["category"] for faq in faqs]))
        }

    def _generate_answer(self, question: dict, product: ProductModel) -> str:
        """Generate contextual answers based on product data."""
        q_text = question["question"].lower()

        if "price" in q_text or "cost" in q_text:
            return f"{product.name} is priced at ₹{product.price}."
        elif "ingredients" in q_text:
            return f"The key ingredients are {', '.join(product.key_ingredients)}."
        elif "benefits" in q_text or "what" in q_text and "do" in q_text:
            return f"It helps with {' and '.join([b.lower() for b in product.benefits])}."
        elif "use" in q_text or "apply" in q_text:
            return product.usage
        elif "skin type" in q_text:
            return f"Suitable for {' and '.join(product.skin_type)} skin."
        elif "side effect" in q_text:
            return product.side_effects
        elif "concentration" in q_text:
            return f"It contains {product.concentration}."
        else:
            return f"For more information about {product.name}, please refer to the product details."
