from abc import ABC, abstractmethod
from threading import Thread, Event
from messaging.message_types import Message, MessageType
from messaging.message_bus import MessageBus
from typing import Dict, Any

class BaseAgent(ABC):
    """Base class for autonomous agents with independent execution."""

    def __init__(self, agent_id: str, message_bus: MessageBus):
        self.agent_id = agent_id
        self.message_bus = message_bus
        self.state: Dict[str, Any] = {}
        self.running = Event()
        self.thread = None

        # Register with message bus
        self.message_bus.register_agent(self.agent_id)

    def start(self):
        """Start autonomous agent execution."""
        self.running.set()
        self.thread = Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        print(f"[{self.agent_id}] Agent started and running autonomously")

    def stop(self):
        """Stop agent execution."""
        self.running.clear()
        if self.thread:
            self.thread.join(timeout=5)
        print(f"[{self.agent_id}] Agent stopped")

    def _run_loop(self):
        """Main execution loop - agent autonomously processes messages."""
        while self.running.is_set():
            message = self.message_bus.receive_message(self.agent_id, timeout=0.5)

            if message:
                print(f"[{self.agent_id}] Received {message.message_type.value} from {message.sender}")
                try:
                    self.handle_message(message)
                except Exception as e:
                    print(f"[{self.agent_id}] Error handling message: {str(e)}")
                    self._send_error(message.sender, str(e), message.conversation_id)

    @abstractmethod
    def handle_message(self, message: Message):
        """Handle incoming message - must be implemented by subclass."""
        pass

    def send_message(self, receiver: str, message_type: MessageType, content: Any, conversation_id: str):
        """Send message to another agent."""
        message = Message(
            sender=self.agent_id,
            receiver=receiver,
            message_type=message_type,
            content=content,
            timestamp=None,
            conversation_id=conversation_id
        )
        self.message_bus.send_message(message)
        print(f"[{self.agent_id}] Sent {message_type.value} to {receiver}")

    def _send_error(self, receiver: str, error: str, conversation_id: str):
        """Send error message."""
        self.send_message(receiver, MessageType.ERROR, {"error": error}, conversation_id)
