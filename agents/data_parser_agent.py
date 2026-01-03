from agents.base_agent import BaseAgent
from messaging.message_types import Message, MessageType
from models.product_model import ProductModel

class DataParserAgent(BaseAgent):
    """Autonomous agent for parsing and validating product data."""

    def handle_message(self, message: Message):
        """Process incoming messages autonomously."""

        if message.message_type == MessageType.REQUEST:
            action = message.content.get("action")

            if action == "parse_data":
                raw_data = message.content.get("data")
                try:
                    print(f"[{self.agent_id}] Parsing product data...")
                    product = ProductModel.from_dict(raw_data)

                    # Validate data
                    self._validate_product(product)

                    # Send parsed data back to requester
                    self.send_message(
                        receiver=message.sender,
                        message_type=MessageType.RESPONSE,
                        content={"product": product.to_dict(), "status": "success"},
                        conversation_id=message.conversation_id
                    )

                    # Broadcast to other agents that might need it
                    broadcast_msg = Message(
                        sender=self.agent_id,
                        receiver="",
                        message_type=MessageType.INFORM,
                        content={"event": "product_parsed", "product": product.to_dict()},
                        timestamp=None,
                        conversation_id=message.conversation_id
                    )
                    self.message_bus.broadcast(broadcast_msg, exclude=[self.agent_id, message.sender])

                except Exception as e:
                    print(f"[{self.agent_id}] Error parsing data: {str(e)}")
                    self._send_error(message.sender, str(e), message.conversation_id)

    def _validate_product(self, product: ProductModel):
        """Validate product data."""
        if not product.name:
            raise ValueError("Product name is required")
        if product.price <= 0:
            raise ValueError("Product price must be positive")
