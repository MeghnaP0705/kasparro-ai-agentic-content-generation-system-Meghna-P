from agents.base_agent import BaseAgent
from messaging.message_types import Message, MessageType
from models.product_model import ProductModel

class QuestionGeneratorAgent(BaseAgent):
    """Autonomous agent for generating user questions."""

    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, message_bus)
        self.product_data = None

    def handle_message(self, message: Message):
        """Process messages autonomously."""

        # Listen for product parsed events from other agents
        if message.message_type == MessageType.INFORM:
            event = message.content.get("event")
            if event == "product_parsed":
                self.product_data = ProductModel.from_dict(message.content["product"])
                print(f"[{self.agent_id}] Received product data via broadcast")

        # Handle direct requests
        elif message.message_type == MessageType.REQUEST:
            action = message.content.get("action")

            if action == "generate_questions":
                if not self.product_data:
                    # Agent autonomously requests missing data
                    print(f"[{self.agent_id}] Don't have product data, requesting...")
                    self.send_message(
                        receiver=message.sender,
                        message_type=MessageType.QUERY,
                        content={"query": "need_product_data"},
                        conversation_id=message.conversation_id
                    )
                    return

                print(f"[{self.agent_id}] Generating questions...")
                questions = self._generate_questions(self.product_data)

                # Send response
                self.send_message(
                    receiver=message.sender,
                    message_type=MessageType.RESPONSE,
                    content={"questions": questions, "count": len(questions), "status": "success"},
                    conversation_id=message.conversation_id
                )

    def _generate_questions(self, product: ProductModel) -> list:
        """Generate categorized questions."""
        questions = []

        # Informational (4 questions)
        questions.extend([
            {"question": f"What is {product.name}?", "category": "Informational"},
            {"question": "What are the key ingredients?", "category": "Informational"},
            {"question": "What skin types is it suitable for?", "category": "Informational"},
            {"question": "What is the concentration?", "category": "Informational"},
        ])

        # Safety (3 questions)
        questions.extend([
            {"question": "Are there any side effects?", "category": "Safety"},
            {"question": "Is it safe for sensitive skin?", "category": "Safety"},
            {"question": "Can I use it with other products?", "category": "Safety"},
        ])

        # Usage (4 questions)
        questions.extend([
            {"question": f"How do I use {product.name}?", "category": "Usage"},
            {"question": "When should I apply it?", "category": "Usage"},
            {"question": "How much should I use?", "category": "Usage"},
            {"question": "Can I use it daily?", "category": "Usage"},
        ])

        # Purchase (3 questions)
        questions.extend([
            {"question": "What is the price?", "category": "Purchase"},
            {"question": "Where can I buy it?", "category": "Purchase"},
            {"question": "Is it worth the price?", "category": "Purchase"},
        ])

        # Comparison (2 questions)
        questions.extend([
            {"question": "How does it compare to other serums?", "category": "Comparison"},
            {"question": f"What makes {product.name} unique?", "category": "Comparison"},
        ])

        return questions
